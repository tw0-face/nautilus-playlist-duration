"""
Add a Nautilus property page to video files to display videos duration.

Author: Mostafa Rashed
"""

from gi.repository import GObject, Gtk, Nautilus
from urllib.parse import urlparse, unquote
import subprocess
import datetime 



class VideoPlaylistPropertyPageProvider(GObject.GObject, Nautilus.PropertyPageProvider):

	def _get_videos_duration(self, files):
		total_s = 0
		n_videos = 0
		for file in files:
			if file.get_mime_type() != 'video/mp4':
				continue
			result = subprocess.run(["ffprobe", "-v", "error", "-show_entries","format=duration", "-of", "default=noprint_wrappers=1:nokey=1", unquote(urlparse(file.get_uri()).path)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
			seconds = float(result.stdout)
			total_s = total_s + seconds
			n_videos = n_videos + 1
		playlist_time = datetime.timedelta(seconds=round(total_s)) 
		return playlist_time, n_videos

	

	def get_property_pages(self, files):
		playlist_time, playlist_videos = self._get_videos_duration(files)
		metadata = {'Number of videos':playlist_videos ,'Playlist Duration':playlist_time}
		property_label = Gtk.Label('Playlist Metadata')
		property_label.show()
		
		grid = Gtk.Grid()
		grid.props.margin_left = 50
		grid.props.margin_top = 20
		
		for row, key in enumerate(['Number of videos', 'Playlist Duration']):
			val = ",".join(metadata[key]) if isinstance(metadata[key], list) else metadata[key] 
			grid.attach(Gtk.Label(f'{key.capitalize()}:    ', xalign=0), 0, row, 1, 1)
			grid.attach(Gtk.Label(val, xalign=0), 1, row, 1, 1)
	
		grid.show_all()
		
		page = Nautilus.PropertyPage(
					name="playlist_metadata",
					label=property_label,
					page=grid)
		return page,
