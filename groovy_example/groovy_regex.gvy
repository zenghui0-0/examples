if (is_unix) {
    ret_pylint = readFile(file: "$path/pylint_check.log")
} else {
    ret_pylint = readFile(file: "$path\\pylint_check.log")
}
def ret_list = ret_pylint.readLines()
def pylint_rate = ""
def first_line_empty = false 
for (line in ret_list) {
    if(line =~ "Your code has been rated at"){
        pylint_rate = line;
    }
}
if (ret_list.size() > 0 && ret_list[0].trim() == "") {
    first_line_empty = true
}
logging.debug("Pylint result: $pylint_rate")
logging.debug("Pylint first line empty? $first_line_empty")
if((pylint_rate =~ "Your code has been rated at 10.00/10") && first_line_empty) {
    logging.debug("Pylint check PASSED.")
}