
mkdir templates 
python3 scaffold.py user username pic:file country_id:references phone email password fm
python3 scaffold.py country name
python3 scaffold.py personne name fm
python3 scaffold.py secrets personne_id:references user_id:references pic:file info_or_gossip
