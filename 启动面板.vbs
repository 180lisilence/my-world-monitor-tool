Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
basePath = fso.GetParentFolderName(WScript.ScriptFullName)
' Start the local python status service silently (no console window)
WshShell.Run "python """ & basePath & "\mc_server.py""", 0, False
' Wait 2 seconds for the service to be ready
WScript.Sleep 2000
' Open the dashboard page (index.html is now the project intro page)
WshShell.Run """" & basePath & "\monitor.html""", 1, False
