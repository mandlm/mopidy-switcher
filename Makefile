
BIN_DIR=/usr/local/bin/mopidy-switcher
SYSV_DIR=/etc/init.d
SYSD_DIR=/etc/systemd/system

install-sysv: service/mopidy-switcher
	install -m 755 -t $(SYSV_DIR) service/mopidy-switcher

install-sysd: service/mopidy-switcher.service
	install -m 644 -t $(SYSD_DIR) service/mopidy-switcher.service

install-switcher: mopidy-switcher.py
	install -m 755 -t $(BIN_DIR) -D mopidy-switcher.py

install: install-sysd install-switcher

uninstall:
	rm -rf $(BIN_DIR)
	rm -f $(SYSV_DIR)/mopidy-switcher
	rm -f $(SYSD_DIR)/mopidy-switcher.service
