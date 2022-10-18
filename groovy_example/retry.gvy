def retry = 5
def retry_interval = 60
while (retry--) {
    try {
        git(branch: "", credentialsId: "", url: "")
        break
    } catch (Exception e) {
        echo "Failed at retry: ${retry}"
    }
    sleep retry_interval
    retry_interval += 60
}