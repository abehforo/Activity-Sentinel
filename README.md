# Activity-Sentinel
Activity Sentinel is basically a system monitoring tool for tracking keystrokes, active windows and network connections. 

The tool will capture keystrokes, including basic keys like Enter and Tab, and records the active window title to show which application is in use. It also logs established network connections, noting local and remote addresses. To ensure secure data handling all captured logs are encrypted before any transmission or storage. Activity Sentinel is designed to be modular with each type of activity logged independently and users can set intervals for periodic logging which on default is set to ten seconds.

Activity Sentinel collects and displays activity data in the terminal at the specified intervals. It includes an optional feature to send encrypted logs to a server which is disabled by default for security and privacy. 

The intended output includes the current active window network connections and typed keystrokes which are displayed in the terminal. After each logging interval the tool clears the keystrokes from memory ensuring they are only temporarily stored while the tool runs.
