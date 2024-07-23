SHELL=/bin/bash
nautilus_path=`which nautilus`
install:
	mkdir -p ~/.local/share/nautilus-python/extensions
	cp nautilus-playlist-duration.py ~/.local/share/nautilus-python/extensions
	@echo 'Restarting nautilus'
	@${nautilus_path} -q||true 

uninstall:
	rm ~/.local/share/nautilus-python/extensions/nautilus-playlist-dur.py
	@echo 'Restarting nautilus'
	@${nautilus_path} -q||true
