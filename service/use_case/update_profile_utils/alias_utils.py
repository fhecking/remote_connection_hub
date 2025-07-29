ALIAS_DEFS = [
    "",
    "#-------------------------------------",
    "# AppManager fuer Interaktion mit Applikationsprozessen",
    "#-------------------------------------",
    "export APPMAN_HOME=${PROJDISC}/appManager",
    "alias appManager=${APPMAN_HOME}/appManager.sh",
    "alias appman=${APPMAN_HOME}/appManager.sh",
    "",
    "#-------------------------------------",
    "# DSM Custom alias",
    "#-------------------------------------",
    "alias tstat=\"ps -auxww|grep tomcat\"",
    "alias jstat=\"ps -auxww|grep jboss\"",
    "alias wstat=\"ps -auxww|grep wildfly\"",
    "alias tlogs=\"cd $PROJDISC/log/tomcat\"",
    "alias jlogs=\"cd $PROJDISC/log/jboss_standalone\"",
    "alias wlogs=\"cd $PROJDISC/log/wildfly_standalone\"",
    "alias control=\"cd $PROJDISC/jboss/jboss-as-7.1.2.Final/inconso_admin\""
]

def get_existing_aliases(lines):
    existing = set()
    for line in lines:
        if line.strip().startswith('alias '):
            alias_name = line.strip().split()[1].split('=')[0]
            existing.add(alias_name)
    return existing

def get_missing_aliases(existing):
    to_add = []
    for alias_def in ALIAS_DEFS:
        alias_name = alias_def.split()[1].split('=')[0]
        if alias_name not in existing:
            to_add.append(alias_def)
    return to_add