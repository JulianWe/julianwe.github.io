# evidence against attacker

**create script that writes the ifconfig CLI output to file**
```sh
cat > interface.sh EOF << 
#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H-%M-%S")
ifconfig > "/Users/jw/launchctl/ifconfig-$DATE"

EOF
```

**create launchctl schduled task that runs our script**
```xml
cat >  ~/Library/LaunchAgents/com.ifconfig.hourly.plist EOF << 
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.ifconfig.hourly.plist</string>
    <key>ProgramArguments</key>
    <array>
      <string>/bin/bash</string>
      <string>/Users/jw/interface.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer> <!-- 3600 Sekunden = 1 Stunde -->
    <key>RunAtLoad</key>
    <true/>
  </dict>
</plist>
EOF
```

**start scheduled task**
```sh
launchctl load ~/Library/LaunchAgents/com.ifconfig.hourly.plist
```

**find uniq ipv6 and mac address evidence from diffrent thread vectors like dnsniff**
```sh
find . -type f -exec grep inet6 {} \; | sort | uniq > ipv6.md

find . -type f -exec grep -oE '([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})' {} \; | sort | uniq > mac.md

cat ipv6.md  | wc -l                                                                                 
1730

cat mac.md | wc -l    
757
```

**using netstat -n**

**on linux check auth.log file for more public ipv4 evidence**

```sh

```