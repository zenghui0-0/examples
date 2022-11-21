def sshExec(script_cmd, ip, credential, returnStatus=false, silent=false) {
    withCredentials([usernamePassword(credentialsId: credential, passwordVariable:"PASSWORD", usernameVariable: "USER")]) {
        def ssh_cmd = "sshpass -p \"\$PASSWORD\" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \$USER@${ip} \"$script_cmd\""
        def ret = util.cmdExecssh_cmd, returnStatus, silent)
        return ret
    }
}