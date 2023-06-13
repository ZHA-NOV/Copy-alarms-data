# Copy-alarms-data

This repository is related to ticket GDS-785

The main traget: Create a service that reads the alarm log files from the boxpc and stores them on the edge for local processsing.

-----------------------------------------------------------
Terminal command for cron job (interval every 2 hours as an example; .sh file path can be different):

crontab -e

0 */2 * * * /bin/bash /home/moxa/logs/smbget.sh
