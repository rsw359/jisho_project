import os
import django
import sys
import xml.etree.ElementTree as ET
import logging

# logging setup for error handling in the function for each entry by name
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# verify that this stand alone script is being run with the correct python interpreter and in the correct directory 
print(sys.executable)

sys.path.append('/Users/roger/allpie/myjisho')
print(sys.path)

# specifying module location for Django to find the app settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'jisho.settings'

# import the project settings module and verify the dir
from jisho import settings
print(settings.BASE_DIR)

# django iniit
django.setup()

# import the models 
from dictionary.models import Entry, KanjiElement, ReadingElement, Sense

# import django settings to check if it's recognized by django
from django.conf import settings
print("Django settings loaded:", settings.INSTALLED_APPS)

# import IntegrityError for handling unique constraint violations in the database(some sense objects have a NoNE type)
from django.db import IntegrityError

def parse_jmdict(xml_file):
    # open the xml and get the root element
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # get the total number of entries and set processed/skipped to 0
    total_entries = len(root.findall('entry'))
    processed = 0
    skipped = 0

    #  start the loop, return a tuple with index and entry object and its text 
    for i, entry in enumerate(root.findall('entry'), 1):
        ent_seq = entry.find('ent_seq').text
        
        # get the entry object and create it if it doesn't exist yet using its unique seq identifier, if it exists, skip it and increment the skipped counter. Returns a tuple of the entry object and a boolean indicating if it was created or not.
        try:
            entry_obj, created = Entry.objects.get_or_create(ent_seq=ent_seq)
            if not created:
                logger.info(f"Entry with ent_seq {ent_seq} already exists. Skipping.")
                skipped += 1
                continue

            # Process k_ele, create the kanji elements and associate them with the entry object
            for k_ele in entry.findall('k_ele'):
                keb = k_ele.find('keb').text
                ke_inf = k_ele.find('ke_inf').text if k_ele.find('ke_inf') is not None else None
                ke_pri = k_ele.find('ke_pri').text if k_ele.find('ke_pri') is not None else None
                
                k_ele_obj, _ = KanjiElement.objects.get_or_create(keb=keb, ke_inf=ke_inf, ke_pri=ke_pri)
                entry_obj.keb_elem.add(k_ele_obj)
            
            # Process r_ele, create the reading elements and associate them with the entry object
            for r_ele in entry.findall('r_ele'):
                reb = r_ele.find('reb').text
                re_nokanji = r_ele.find('re_nokanji') is not None
                re_restr = r_ele.find('re_restr').text if r_ele.find('re_restr') is not None else None
                re_inf = r_ele.find('re_inf').text if r_ele.find('re_inf') is not None else None
                re_pri = r_ele.find('re_pri').text if r_ele.find('re_pri') is not None else None
                
                r_ele_obj, _ = ReadingElement.objects.get_or_create(reb=reb, re_nokanji=re_nokanji, re_refr=re_restr, re_inf=re_inf, re_pri=re_pri)
                entry_obj.reb_elem.add(r_ele_obj)
            
            # Process sense
            for sense in entry.findall('sense'):
                gloss = ', '.join([g.text for g in sense.findall('gloss') if g.text])
                pos = ', '.join([p.text for p in sense.findall('pos') if p.text])
                xref = ', '.join([x.text for x in sense.findall('xref') if x.text])
                ant = ', '.join([a.text for a in sense.findall('ant') if a.text])
                field = ', '.join([f.text for f in sense.findall('field') if f.text])
                lsource = ', '.join([l.text for l in sense.findall('lsource') if l.text])
                misc = ', '.join([m.text for m in sense.findall('misc') if m.text])
                example = ', '.join([e.text for e in sense.findall('example') if e.text])
                
                # create the sense object or raise exception if sense is NONE
                try:
                    sense_obj = Sense.objects.create(gloss=gloss, pos=pos, xref=xref, ant=ant, field=field, lsource=lsource, misc=misc, example=example)
                    entry_obj.sense.add(sense_obj)
                except Exception as e:
                    logger.error(f"Error creating Sense for entry {ent_seq}: {str(e)}")
            # save the object and increment the processed counter
            entry_obj.save()
            processed += 1

        # if the object already exists, log it and increment the skipped counter then continue. Keeps the process from crashing
        except IntegrityError:
            logger.error(f"Error processing entry with ent_seq {ent_seq}. Skipping.")
            skipped += 1
            continue
        #log every thousand entries in the console 
        if i % 1000 == 0:  # Log progress every 1000 entries
            logger.info(f"Processed {i} out of {total_entries} entries")
            
    # log the completed processed and skipped entries
    logger.info(f"Parsing completed. Processed: {processed}, Skipped: {skipped}, Total: {total_entries}")

# Call the function with the path to XML file
parse_jmdict('/Users/roger/allpie/myjisho/jisho/JMdict_e_examp')