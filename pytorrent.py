import libtorrent as lt
import time
import sys
from subprocess import check_output, call

filename=sys.argv[1]

SavePath = "./"
#TorrentFilePath = "./"

state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating'] 

starttime = time.time()
ses = lt.session()
#ses.listen_on(6881, 6891)
ses.start_dht()

def err(er):
	print er.args      # arguments stored in .args
	print er
	return 1

def getMetadata():
	global handle
	while (not handle.has_metadata()):
		call('clear',shell=True)
		s = handle.status()
		print ('(peers: %d, connections: %d) %s' % (s.num_peers, s.num_connections, state_str[s.state]))
		time.sleep(5)

def bitmap(pieces_list):
	a=''
	for e in pieces_list:
		if e:
			a=a+'X'
		else:
			a=a+'.'
	return a

def start_download():
	global handle
	print ('starting torrent download...')
	handle.set_sequential_download(True)

	while (handle.status().state != lt.torrent_status.seeding):
		call('clear',shell=True)
		s = handle.status()
		print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.3f' % \
	                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
	                s.num_peers, state_str[s.state], s.total_download/1000000)
		print ('pieces:')
		print (bitmap(s.pieces))
		info=''

		if (handle.status().state==lt.torrent_status.downloading and ".avi" in file.path and info==''):
			try:
				info=check_output(["ffmpeg", "-hide_banner", "-i", file.path, "-f", "ffmetadata", "-"])
				print (info)
			except:
				info=''
		time.sleep(5)
try:
	if ".magnet" in filename:
		print "processing magnet link..." 
	
		fo = open(filename, "r+")
		magneturi = fo.read();
		params = { 'save_path': SavePath, 'storage_mode': lt.storage_mode_t.storage_mode_sparse}
		handle = lt.add_magnet_uri(ses, magneturi, params)
		getMetadata()

		runtime=time.time()-starttime
		print ("runtime:")
		print (str(runtime))
		#print 'saving torrent file here : ' + TorrentFilePath + " ..."
		torinfo = handle.get_torrent_info()
		fs = lt.file_storage()
		for file in torinfo.files():
			fs.add_file(file)
			print (file.path)
		'''
		#Creating torrent if needed
		torfile = lt.create_torrent(fs)
		torfile.set_comment(torinfo.comment())
		torfile.set_creator(torinfo.creator())
		f = open(TorrentFilePath + "torrentfile.torrent", "wb")
		f.write(lt.bencode(torfile.generate()))
		f.close()
		'''
		fo.close()
		#print ("saved and closing...")
	else:
		print ("processing torrent file...")

		fo = open(filename, "rb")
		e = lt.bdecode(fo.read())
		info = lt.torrent_info(e)

		for file in info.files():
			#find if it is a movie
			if ".avi" in file.path:
				fileNameSaved=file.path
			print (file.path)
		params = {'save_path': SavePath, 'storage_mode': lt.storage_mode_t.storage_mode_sparse, 'ti': info}
		handle = ses.add_torrent(params)
		fo.close()
	time.sleep(2)
	start_download()	
	
except Exception as er:
	err(er)
	print ("file io error")

runtime=time.time()-starttime
print ("runtime")
print (str(runtime))