import java.lang.Throwable

logging = load "modules/log/logging.gvy"

def go(config = null, global_config = null) {
    logging.go(config, global_config)
    stage("Init") {
    }
    def parallel_main = [:]
    parallel_main["main"] = {
        stage("PreCheck") {
        }
        stage("Build") {
        }
        stage("Test") {
        }
        stage("PostCheck") {
        }
    }
    parallel_main["mainMonitor"] = {
    }
    parallel_master.failFast = true
    try {
        parallel parallel_master
    } catch (hudson.AbortException e){
        logging.error(e.toString())
    } catch (Exception e) {
        util.setFailure(global_config, "Exception in main.gvy, Exception: ${e.toString()}")
    } catch (Throwable e) {
    }
    

}