# Put into  seperate script - reuse by handler!
def read_intent_mapping(filename):
    mapping = {}
    content = None
    with open(filename, 'r') as file:
        content = file.readlines()
    if content is None: 
        return False #Put proper exception here
    content = [x.strip('\n') for x in content] 
    for c in content:
        #print(c)
        line = c.split(',')
        #print(line)
        mapping[int(line[1])] = line[0]
    return mapping

# Put into  seperate script - reuse by handler!
def read_hotword_mapping(filename):
    mapping = {}
    content = None
    with open(filename, 'r') as file:
        content = file.readlines()
    if content is None: 
        return False #Put proper exception here
    content = [x.strip('\n') for x in content] 
    for c in content:
        #print(c)
        line = c.split(',')
        #print(line)
        mapping[(line[0].upper())] = line[1]
    return mapping


#def read_label_date_mapping(filename):
