# easycut-smartbench
Console UI for YetiTool's SmartBench


Buffer logging:
- Output of grbl serial char and line buffer now standard in 'go' screen.
- To enable writing to file, tap "buffer log" toggle button in dev tab. (Blue=on)
	- WARNING: File overwritten on the start of next stream job.
	
Virtual HW:
- Designed for use of Arduino without any switches
- Essential, before enabling: On arduino, to avoid door error, connect Analouge 11 to GND (think E must have inverted the setting in the config file, was surprised to see this error)
- WARNING: toggle effects are persistent in grbl. So ensure to toggle state back to required status before powering down device to avoid unexpected results on startup (toggle state defaults to disabled, regardless of persistent settings. If this happens, just flick the toggle at least once to sync toggle with state)
- WARNING: In virtual mode, Mpos will default to 0,0,0 so 
	- Head will be at wrong end of bed to start with
	- Running virtual hw with actual machine plugged in will cause plenty of conflict :-) Don't!
- After clicking play button to enter the go screen, ignore popup errors and click on 'continue anyway'