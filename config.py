import configparser

rule_file = configparser.ConfigParser()
rule_file.read("./config.ini", "UTF-8")
