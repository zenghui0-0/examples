import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException







def go(){
    stage("BuildPrepare") {}
	parallel_build["Build On Node 1"] = {
	    stage("PreBuild") {
		}
		stage("BuildExecute") {
		}
	}
	parallel_build["BuildMonitor"] = {}
    parallel_build.failFast = true
    try{
        parallel parallel_build
        ret["StatusCode"] = 0
    } catch (FlowInterruptedException e) {
        logging.error("Build stage detected an FlowInterruptedException exception mostlikely caused by abortion, ending module gracefully")
        util.setAbort(global_config)
    } catch (Exception e) {
        // setFailure
        error(e.toString())
    }
}