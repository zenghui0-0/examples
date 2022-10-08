config.each { c ->
    if (c.key.startsWith('Test')) {
        test_name = c.key
        logging.debug("Start deal with Test: ${test_name}")
    }
}
