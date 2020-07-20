#!/usr/bin/env python3
###################################################################################################
###-           {API that sends Missions}                                                       ##-#
###-Mission Line Actions                                                                       ##-#
###-Authors:   Luis Monteiro                                                                   ##-#
###-Reviewers:                                                                                 ##-#
###################################################################################################

###################################################################################################
# -------------------------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------------------------
###################################################################################################
# external
from collections import OrderedDict

# framework
from robotworker.api import Api as Base
from robotworker.api import Pattern

# internal
from .terminal   import Terminal

###################################################################################################
# -------------------------------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------------------------------
###################################################################################################
class CommandFailed(RuntimeError):
    def __init__(self, step, report):
        from sys import stderr
        from sys import stdout
        # update runtime exception
        super().__init__(f'Step {step} Failed')
        # print stdout
        for line in report.get('out', []):
            print(line, file=stdout)
        # print stderror
        for line in report.get('err', []):
            print(line, file=stderr)
            
###################################################################################################
# -------------------------------------------------------------------------------------------------
# Commander Api
# -------------------------------------------------------------------------------------------------
###################################################################################################
class Api(Base):
    '''
        :description:			Api for Mission Line 
        :params:				None
        :return:				Object terminator API 
    '''
    #####################################################################################
    # -----------------------------------------------------------------------------------
    #  Constructor
    #  @conf: configuration
    #  @ext : extensions 
    # -----------------------------------------------------------------------------------
    def __init__(self, conf={}, ext=[]):
        # load base
        super().__init__(conf, ext)
        # load missions
        self._load_missions(conf.get('missions', {}))
        # load propreties
        self.__settings = conf.get('properties', {})

    #####################################################################################
    # -----------------------------------------------------------------------------------
    # load missions
    # -----------------------------------------------------------------------------------
    def _load_missions(self, configuration):
        class Mission():
            def __init__(self, func, conf):
                self.__func = func
                self.__conf = conf
            def __call__(self, *args, **kargs):
                return self.__func(self.__conf, *args, **kargs)
        for name, params in configuration.items():
            setattr(self, name, Mission(self._run_mission, params).__call__)
        
    #####################################################################################
    # -----------------------------------------------------------------------------------
    # run mission
    # -----------------------------------------------------------------------------------
    def _run_mission(self, config, *args, **kargs):
        # build context & process
        context  = self.__build_context (config.get('context'   , {}), args, kargs)
        settings = self.__build_settings(config.get('properties', {}), context)
        process  = self.__build_process (config.get('script'    , {}), context)
        # create terminal
        terminal = Terminal(settings.get('workspace', '.'))
        # run process steps
        report = {}
        for execute, retries, require in process:
            # run step
            good, cmd, output = terminal(execute, retries)
            # process report
            result = self.__build_result(output, settings)
            if good or not require:
                report[cmd] = result
            else:
                raise CommandFailed(cmd, result) 
        return report

    #####################################################################################
    # -----------------------------------------------------------------------------------
    # build context
    # -----------------------------------------------------------------------------------
    def __build_context(self, conf, args, kargs):
        # use current environment 
        context = self.get_context()
        # update with command config
        context.update(conf)
        # update with command list arguments
        context.update(zip(conf, args))
        # update with command keys arguments
        context.update(kargs)
        return context

    #####################################################################################
    # -----------------------------------------------------------------------------------
    # build settings
    # -----------------------------------------------------------------------------------
    def __build_settings(self, conf, ctxt):
        settings = self.__settings.copy()
        settings.update(conf)
        out = {}
        for k, v in settings.items():
            if isinstance(v, str):
                out[k] = Pattern(v).substitute(ctxt)
                continue
            out[k] = v
        return out

    #####################################################################################
    # -----------------------------------------------------------------------------------
    # build process
    # -----------------------------------------------------------------------------------
    def __build_process(self, conf, ctxt):
        steps = []
        for step in (conf if isinstance(conf, list) else [conf]):
            try:
                if isinstance(step, (dict, OrderedDict)):
                    steps.append((
                        Pattern(step['execute']).substitute(ctxt), 
                        step.get('retries', 0),
                        step.get('require', True)))
                    continue
                if isinstance(step, str):
                    steps.append((
                        Pattern(step).substitute(ctxt), 0, True))
                    continue
            except:
                pass
            self._log.warning(f'invalid step {step}')
        return steps
    
    #####################################################################################
    # -----------------------------------------------------------------------------------
    # build report
    # -----------------------------------------------------------------------------------
    def __build_result(self, output, settings):
        lim = settings.get('scrollback', 1000000) 
        # filter by size
        out = output.get('out', [])[-lim:]
        err = output.get('err', [])[-lim:]
        # filter tags
        res = {}
        if out: res['out'] = out
        if err: res['err'] = err
        # return result
        return res

###################################################################################################
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------
###################################################################################################
