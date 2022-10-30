
def go(){
    def cn = env.GERRIT_CHANGE_NUMBER
	def patch_map = gerrit_Query(nr)
	if (patch_map == null) {
        logging.error("[Gerrit monitor] null when Query gerrit")
        return -1
    }
	// if cannot connect to Gerrit for 5 whole mins (5 mins retry in gerritQuery)
    if (patch_map == null) {
        util.setAbort(global_config, "[Gerrit monitor] null patch_map when calling gerritQuery")
        return [
            "StatusCode" : STATUS.ABORT
        ]
    }

    // if Gerrit API failed
    if (patch_map.containsKey("type") && patch_map.type == "error") {
        util.setFailure(global_config, "[Gerrit monitor] Gerrit API failed, error message: ${patch_map.message}")
        return [
            "StatusCode" : STATUS.ABORT
        ]
    }

     /* If patchset valid */
     /* check the patch if verified -1 or abandoned */
    if (config.containsKey("checkPatchValid") && config["checkPatchValid"]["Enabled"] == true) {
        if (!isPatchValid(patch_map)) {
            util.setAbort(global_config, config["checkPatchValid"]["Message"])
            return [
                "StatusCode" : STATUS.ABORT
            ]
        }
    }

    // check if the patchset is based on latest code, if not rebase automatically if no conflict
    if (config.containsKey("AutoRebase") && config["AutoRebase"] == true) {
        def res_patch = ""
        dir("modules/commit_message") {
            res_patch = sh(script:"python3 gerrit_patch.py pre_submission_workflow ${env.GERRIT_CHANGE_NUMBER} ${GERRIT_PATCHSET_NUMBER}", returnStdout: true).trim()
        }
        logging.debug("check merge status:${res_patch}")
        if (res_patch.contains('Error')) {
            logging.debug("Merge status contain Error")
            util.setAbort(global_config, "Rebase Failure")
                return [
                    /* -2 as abort */
                    "StatusCode" : STATUS.ABORT,
                ]
        } else if (res_patch.contains('Success')) {
            if (res_patch.contains('Rebase')) {
                logging.debug("Merge status contain Rebase")
                util.setAbort(global_config, "Rebase Successfully, new patchset generated")
                return [
                    /* -2 as abort */
                    "StatusCode" : STATUS.ABORT,
                ]
            }
        }
    }

    /* If patchset updated */
    /* check if the patchset is updated*/
    if (config.containsKey("checkPatchUpToDate") && config["checkPatchUpToDate"]["Enabled"] == true) {
        if (!isPatchUpToDate(patch_map)) {
            util.setAbort(global_config, config["checkPatchUpToDate"]["Message"])
            return [
                "StatusCode" : STATUS.ABORT
            ]
        }
    }

    /* If patchset on the top */
    if (config.containsKey("checkPatchOnTop") && config["checkPatchOnTop"]["Enabled"] == true) {
        if (!isPatchOnTop(patch_map, global_config)) {
            util.setAbort(global_config, config["checkPatchOnTop"]["Message"])
            return [
                "StatusCode" : STATUS.ABORT
            ]
        }
    }

    /* If child patchset valid */
    if (config.containsKey("checkChildValid") && config["checkChildValid"]["Enabled"] == true) {
        if (!isChildValid(patch_map, global_config)) {
            util.setAbort(global_config, config["checkChildValid"]["Message"])
            return [
                "StatusCode" : STATUS.ABORT
            ]
        }
    }

    return [
        "StatusCode" : STATUS.SUCCESS,
        "Message" : "Pass"
    ]

	
}

def gerrit_Query(nr, global_config) {
    def json_str = queryDataFromGerrit(nr, global_config)
    def json = null
    def re_try = 0

    while (!json && re_try < 5) {
        if (json_str) {
            json =  json_parser.parseFromStr(json_str)
            if (!json.containsKey("currentPatchSet")) {
                json = null
            }
        }
        if (!json) {
            sleepsec(60)
            json_str = queryDataFromGerrit(nr, global_config)
            re_try++
        }
    }
    return json
}

String queryDataFromGerrit(nr, retry = 10) {
    def cid = ""
    def ret = null
    withCredentials([sshUserPrivateKey(credentialsId: cid, keyFileVariable:"SSH_KEY", usernameVariable: "SSH_USER")]) {
        while (ret == null && retry > 0) {
            ret = util.cmdExec("""ssh -o StrictHostKeyChecking=no -i \$SSH_KEY \$SSH_USER@git.amd.com -p 29418 gerrit query --format=JSON --dependencies --current-patch-set change:${nr}""")
            if (ret == null) {
                sleepsec(30)
                retry --
            }
        }
    }

    if (!ret) {
        logging.error("Can't get information from gerrit for change ${nr}")
    }

    return ret
}
