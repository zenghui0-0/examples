import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException

def buildStages(config, global_config, server) {
    def stages = {
        stage("Server Execute") {
            waitUntil{
            }
            def parallel_in_node = [:]
            parallel_in_node["On ${server["Name"]}"] = {
                node(server["Name"]) {
                    stage("PreBuild") {
                    }
                    stage("BuildExe") {
                    }
                    stage("PostBuild") {
                    }
                }
            }
            lock(server["Name"]) {
                while (retry > 0) {
		    retry --
                    try {
                        parallel parallel_in_node
                        break
                    } catch (FlowInterruptedException e) {
                    } catch (Exception e) {
                    }
                    server['StatusCode'] = "Success" // will stop all tests on this node
                }
            }
        }
    }
    return stages
}

def buildInParallel(config, global_config) {
    def parallel_build = [:]
    def no_server = 0

    /* For each server, we parallel run */
    for (Map server : server_list) {
        /* define the parallel */
        parallel_build["Build On Node ${no_server}"] = buildStages(config, global_config, server)
        no_server ++
    }
    return parallel_build
}

def go(){
    stage("BuildPrepare") {}
	def parallel_build = buildInParallel(config, global_config)
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
