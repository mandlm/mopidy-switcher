
BIN_DIR=/usr/local/bin/mopidy-switcher
SYSV_DIR=/etc/init.d
SYSD_DIR=/etc/systemd/system

install-sysv: service/mopidy-switcher
	install service/mopidy-switcher $(SYSV_DIR)

install-sysd: service/mopidy-switcher.service
	install service/mopidy-switcher.service $(SYSD_DIR)

install-switcher: mopidy-switcher.py
	install -D mopidy-switcher.py $(BIN_DIR)

install: install-sysd install-switcher

uninstall:
	rm -rf $(BIN_DIR)
	rm -f $(SYSV_DIR)/mopidy-switcher
	rm -f $(SYSD_DIR)/mopidy-switcher.service
