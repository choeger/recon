from recon.wall import WallReader, WallWriter
from recon.meld import MeldReader, MeldWriter

def wall2meld(wfp, mfp):
    wall = WallReader(wfp)
    meld = MeldWriter(mfp)

    objects = {}
    tables = {}

    # Create definitions for meld

    # TODO: Process metadata
    # TODO: Add option to do overthing in memory? (to avoid multiple reads)
    #       Simple implementation...copy wfp into a StringIO buffer and use that.

    # Start with objects
    for objname in wall.objects():
        objects[objname] = meld.add_object(objname)

    # Then do tables
    for tabname in wall.tables():
        table = wall.read_table(tabname)
        tables[tabname] = meld.add_table(name=tabname, signals=table.signals());
        mtable = tables[tabname]
        for alias in table.aliases():
            mtable.add_alias(alias, 
                             of=table.alias_of(alias),
                             scale=table.alias_scale(alias),
                             offset=table.alias_offset(alias))
    
    # Now that all definitions are made, we can finalize the meld
    meld.finalize()

    # Write actual data in meld
    for objname in wall.objects():
        obj = wall.read_object(objname)
        objects[objname].write(**obj)

    for tabname in wall.tables():
        wtable = wall.read_table(tabname)
        mtable = tables[tabname]
        for signal in wtable.signals():
            mtable.write(signal, wtable.data(signal));
