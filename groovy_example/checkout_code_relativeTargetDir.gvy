repo = "ssh://gerritgit/a/ec/tools/ci"
checkout([
    $class: 'GitSCM',
    branches: [[name: "${branch}"]],
    doGenerateSubmoduleConfigurations: false,
    extensions: [[
	    $class: 'RelativeTargetDirectory',
		relativeTargetDir: targetDir
	]],
    submoduleCfg: [],
    userRemoteConfigs: [[
	    credentialsId: credentials_id,
		url: repo
	]]
])