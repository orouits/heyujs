import re
import subprocess
import logging

# ------------------------------------------------
# utils functions
# ------------------------------------------------

def filterList(inlines, regex=None, subex=None):
    outlines = []
    pat = None
    if regex:
        pat = re.compile(regex)
    #print('filterList\n')
    for line in inlines:
        line = line.strip()
        if line:
            if pat is not None:
                if pat.match(line):
                    if subex is not None:
                        line = pat.sub(subex, line)
                        #print('filterList-R>' + line)
                        outlines.append(line)
                    else:
                        #print('filterList-M>' + line)
                        outlines.append(line)
            else:
                #print('filterList-A>' + line)
                outlines.append(line)
    return outlines


def loadFile2List(fname):
    lines = []
    #print('loadFile2List\n')
    with open(fname, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                #print('loadFile2List-A>' + line)
                lines.append(line)
    return lines

def runCommand2List(cmd):
    print('Command2List ' + cmd )
    output = subprocess.check_output(cmd, shell=True, encoding='utf-8').strip()
    print('Command2List out: ' + output)
    lines = []
    for line in output.split('\n'):
        line = line.strip()
        if line:
            #print('Command2List-A>' + line)
            lines.append(line)
    return lines

patSpaceSep = re.compile('\s+')
patScheduleSep = re.compile('[\s#-]+')
patCommentSep = re.compile('\s*#\s')

# ------------------------------------------------
# Resource classes
# ------------------------------------------------
class Status:
    status = False
    def __init__(self, status):
        self.status = (status == True)
        
    @classmethod    
    def fromDict(cls, data):
        return cls(data['status'])
        
    def __repr__(self):
        return "'Status:{0}".format(self.status)

        
    
class Alias:
    id = ''
    unitid = ''
    type = ''
    grouptag = ''
    
    def __init__(self, id, unitid, type, grouptag):
        self.id = id.upper()
        self.unitid = unitid
        self.type = type
        self.grouptag = grouptag

    @classmethod    
    def fromDict(cls, data):
        return cls(data['id'], data['unitid'], data['type'], data['grouptag'])

    @classmethod    
    def fromConfLine(cls, line):
            items = patCommentSep.split(line)
            comment = items[1] if len(items) > 1 else ""
            items = patSpaceSep.split(items[0])                
            return cls(items[1], items[2], items[3], comment)

    def toConfLine(self):
        return "ALIAS {} {} {} #{}".format(self.id, self.unitid, self.type, self.grouptag)
        
    def __repr__(self):
        return "'Alias:{},{},{},{}'".format(self.id, self.unitid, self.type, self.grouptag)


class Setting:
    id = ''
    val = ''
    comment = ''

    def __init__(self,id, val, comment):
        self.id = id.upper()
        self.val = val
        self.comment = comment

    @classmethod    
    def fromDict(cls, data):
        return cls(data['id'], data['val'], data['comment'])
        
    @classmethod    
    def fromConfLine(cls, line):
            items = patCommentSep.split(line)
            comment = items[1] if len(items) > 1 else ""
            items = patSpaceSep.split(items[0])                
            return cls(items[0], items[1], comment)
        
    def toConfLine(self):
        return "{} {} #{}".format(self.id, self.val, self.comment)
        
    def __repr__(self):
        return "'Setting:{},{},{}'".format(self.id, self.val, self.comment)


class Macro:
    id = ''
    misc = ''
    status = ''
    unitid = ''

    def __init__(self, id, misc, status, unitid):
        self.id = id.upper()
        self.misc = misc
        self.status = status
        self.unitid = unitid        

    @classmethod    
    def fromDict(cls, data):
        return cls(data['id'], data['misc'], data['status'], data['unitid'])
        
    @classmethod    
    def fromConfLine(cls, line):
            items = patCommentSep.split(line)
            comment = items[1] if len(items) > 1 else ""
            items = patSpaceSep.split(items[0])                
            return cls(items[1], items[2], items[3], items[4])

    def toConfLine(self):
        return "macro {} {} {} {}".format(self.id, self.misc, self.status, self.unitid)
        
    def __repr__(self):
        return "'Macro:{},{},{},{}'".format(self.id, self.misc, self.status, self.unitid)

class Schedule:
    id = ''
    weekdays = ''
    fromDate = ''
    toDate = ''
    fromTime = ''
    toTime = ''
    macroOn = ''
    macroOff = ''
    enabled = False
    
    def __init__(self,id, weekdays, fromDate, toDate, fromTime, toTime, macroOn, macroOff, enabled):
        self.id = str(id).upper()
        self.weekdays = weekdays
        self.fromDate = fromDate
        self.toDate = toDate
        self.fromTime = fromTime
        self.toTime = toTime
        self.macroOn = macroOn
        self.macroOff = macroOff
        self.enabled = enabled
        
    @classmethod    
    def fromDict(cls, data):
        return cls(data['id'], data['weekdays'], data['fromDate'], data['toDate'], data['fromTime'], data['toTime'], data['macroOn'], data['macroOff'], data['enabled'])
 
    @classmethod    
    def fromConfLine(cls, id, line):
            enabled = True
            if line[0] == "#":
                enabled = False
                line = line[1:]
            items = patScheduleSep.split(line)
            if items[8]: id = items[8]
            return cls(id, items[1], items[2], items[3], items[4], items[5], items[6], items[7], enabled)

    def toConfLine(self):
        if self.enabled:
            return "timer {} {}-{} {} {} {} {} # {}".format(self.weekdays, self.fromDate, self.toDate, self.fromTime, self.toTime, self.macroOn, self.macroOff, self.id)
        return "#timer {} {}-{} {} {} {} {} # {}".format(self.weekdays, self.fromDate, self.toDate, self.fromTime, self.toTime, self.macroOn, self.macroOff, self.id)
        
    def __repr__(self):
        return "'Schedule:{},{},{},{},{},{},{},{},{}'".format(self.id, self.weekdays, self.fromDate, self.toDate, self.fromTime, self.toTime, self.macroOn, self.macroOff, self.enabled)

class Unit:
    id = ''
    level = 0
    on = False
    unitid = ''
    type = ''
    grouptag = ''   
    
    def __init__(self, id, level, alias = None):
        self.id = id.upper()
        self.level = int(level)
        self.on = int(level) > 0
        if alias is None:
            self.unitid = id
            self.type = ''
            self.grouptag = ''
        else:
            self.unitid = alias.unitid
            self.type = alias.type
            self.grouptag = alias.grouptag
            
    @classmethod    
    def fromDict(cls, data):
        return cls(data['id'], data['level'])
        
    def __repr__(self):
        return "'Unit:{0},{1},{2},{3},{4},{5}'".format(self.id, self.level, self.on, self.unitid, self.type, self.grouptag)

class Command:
    cmd = ''
    excmd = ''
    rc = 0
    output = ''

    def __init__(self, cmd, output):
        self.cmd = cmd
        self.excmd = ''
        self.rc = 0
        self.output = output
        
    @classmethod    
    def fromDict(cls, data):
        return cls(data['cmd'], data['output'])

    def __repr__(self):
        return "'Command:{0},{1},{2},{3}'".format(self.cmd, self.excmd, self.rc, self.output)

# ------------------------------------------------
# heyu class
# ------------------------------------------------
        
class Heyu:
    settings = {}
    aliases = {}
    schedules = {}
    macros = {}
    
    heyucmd = ''
    heyuconf = '' 
    heyusconf = ''
    
    def __init__(self, heyucmd, heyuconf, heyusconf):
        self.heyucmd = heyucmd + ' -c ' + heyuconf + ' -s ' + heyusconf
        self.heyuconf = heyuconf
        self.heyusconf = heyusconf
        self.loadConfig()
        self.loadScheduleConfig()

    def loadConfig(self):
        lines = filterList(loadFile2List(self.heyuconf),'(?!^#.*$)') #ignore comments lines
        for line in lines:            
            if line.startswith('ALIAS'):
                alias = Alias.fromConfLine(line)
                self.aliases[alias.id] = alias
            else:
                setting = Setting.fromConfLine(line)
                self.settings[setting.id] = setting
        self.postConfig("#HEYUCMD", self.heyucmd)
        self.postConfig("#HEYUCONF", self.heyuconf)
        self.postConfig("#HEYUSCONF", self.heyusconf)
        #print("Settings: {}".format(len(self.settings)))
        #print("Aliases: {}".format(len(self.aliases)))

    def loadScheduleConfig(self):
        lines = filterList(loadFile2List(self.heyusconf),'^(timer|#timer|macro)\s+.*$')
        for line in lines:
            if line.startswith('macro'):
                macro = Macro.fromConfLine(line)
                self.macros[macro.id] = macro
            else:
                schedule = Schedule.fromConfLine(len(self.schedules), line)
                self.schedules[schedule.id] = schedule            
        #print("Schedules: {}".format(len(self.schedules)))
        #print("Macros: {}".format(len(self.macros)))
    
    def postConfig(self, id, val):
        if id not in self.settings.keys():
            self.settings[id] = Setting(id, val, "Added for comment")

    def saveConfig(self):
        with open(self.heyuconf, 'w') as file:
            file.write('# SETTINGS' + '\n')        
            for setting in self.settings.values():
                file.write(setting.toConfLine() + '\n')        
            file.write('# ALIASES' + '\n')        
            for alias in self.aliases.values():
                file.write(alias.toConfLine() + '\n')
            file.write('# END' + '\n')        

    def saveScheduleConfig(self):
        with open(self.heyusconf, 'w') as file:
            file.write('# MACROS' + '\n')        
            for macro in self.macros.values():
                file.write(macro.toConfLine() + '\n')
            file.write('# SCHEDULES' + '\n')        
            for schedule in self.schedules.values():
                file.write(schedule.toConfLine() + '\n')
            file.write('# END' + '\n')        
            

    def execHeyu(self, heyuCommand, regex=None, subex=None):
        return filterList(runCommand2List(self.heyucmd + ' ' + heyuCommand), regex, subex)
    
    def getStatus(self):
        return Status(self.execHeyu('enginestate', '^[01]$')[0] == "1")

     
    def getSettings(self):
        return list(self.settings.values())
     
    def getSetting(self, id):
        return self.settings[str(id)]

     
    def upsertSetting(self, id, data):
        data['id'] = id.upper()
        setting = Setting.fromDict(data)
        self.settings[setting.id] = setting
        self.saveConfig()
        return setting
     
    def getAliases(self):
        return list(self.aliases.values())
     
    def getAlias(self, id):
        id = id.upper()
        return self.aliases[id]
     
    def upsertAlias(self, id, data):
        data['id'] = id.upper()
        alias = Alias.fromDict(data)
        self.aliases[alias.id] = alias
        self.saveConfig()
        return alias
     
    def deleteAlias(self, id):
        id = id.upper()
        self.aliases.remove(id)
        selft.saveConfig()
        return id
    
     
    def getMacros(self):
        return list(self.macros.values())
    
     
    def getMacro(self, id):
        id = id.upper()
        return self.macros[id]
    
     
    def upsertMacro(self, id, data):
        data['id'] = id.upper()
        macro = Macro.fromDict(data)
        self.macros[macro.id] = macro
        self.saveScheduleConfig()
        return macro
    
     
    def deleteMacro(self, id):
        id = id.upper()
        del self.macros[id]
        self.saveScheduleConfig()
        return id
    
     
    def getSchedules(self):
        return list(self.schedules.values())
    
     
    def getSchedulesFile(self):
        return loadFile2List(self.heyusconf)
     
    def getSchedule(self, id):
        id = id.upper()
        return self.schedules[id]
    
     
    def upsertSchedule(self, id, data):
        data['id'] = id.upper()
        schedule = Schedule.fromDict(data)
        self.schedules[schedule.id] = schedule
        self.saveScheduleConfig()
        return schedule
    
     
    def deleteSchedule(self, id):
        id = id.upper()
        del self.schedules[id]
        self.saveScheduleConfig()
        return id

    def getUnits(self, housecode):
        units = []
        
        if not housecode:                        
            for id in self.aliases:
                units.append(self.getUnit(id))
        elif housecode == 'ALL':
            patSpaceSep = re.compile('\s+')
            lines = self.execHeyu('show dim', '^\s*([A-P])\s+(.*)$', '\\1 \\2')          
            for line in lines:
                #H 0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
                items = patSpaceSep.split(line)
                hcode = items[0]
                for i in range(1, 16):
                    units.append(Unit(hcode + str(i), items[i]))
        else:
            patSpaceSep = re.compile('\s+')
            lines = self.execHeyu('show dim', '^\s*(' + housecode + ')\s+(.*)$', '\\1 \\2')          
            for line in lines:
                #H 0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
                items = patSpaceSep.split(line)
                hcode = items[0]
                for i in range(1, 16):
                    units.append(Unit(hcode + str(i), items[i]))        
        return units

    def getUnit(self, id):
        id = id.upper()
        out = self.execHeyu("dimlevel " + id)[0]
        return Unit(id, out, self.aliases[id] if id in self.aliases else None)

    def setUnitStatus(self, id, data):
        print('DATA: ' + str(data))
        data['id'] = id.upper()

        if 'level' in data and 0 < data['level'] < 100:
            self.execHeyu('dim ' + id + ' ' + data['level'])
        elif 'on' in data and data['on']:
            self.execHeyu('on ' + id)
        else:
            self.execHeyu('off ' + id)
        
        return self.getUnit(id)

    def setUnitModule(self, id):
        id = id.upper()
        # set module adress in programming mode
        self.execHeyu('on ' + id)
        self.execHeyu('on ' + id)
        # close module programming mode
        self.execHeyu('off ' + id)
        self.execHeyu('off ' + id)
        self.execHeyu('off ' + id)
        self.execHeyu('off ' + id)
        self.execHeyu('off ' + id)
        return self.getUnit(id);

    def getCommands(self):
        return self.execCommand("help")

    def execCommand(self, cmd):
        if re.match('[,;]', cmd):
            return Command(cmd, 'INVALID COMMAND!')
        lines = self.execHeyu(cmd)
        output = ''
        for line in lines:
            output += line + '\n'              
        return Command(cmd, output)
    
   
heyu = Heyu('/usr/local/bin/heyu', '/var/www/html/heyujs/api/x10config', '/var/www/html/heyujs/api/x10.sched')
