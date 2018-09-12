; This file is Copyright 2006 Darryl A. Dixon <esrever_otua@pythonhacker.is-a-geek.net>
;
; It is part of, and covered by, the same licensing terms as Bible Dave.
;
; bibledave.nsi

; You can use this file along with setup.py to build an installable,
; stand-alone Bible Dave program, with no external Python dependencies.
; To do this, on a properly configured Windows PC run:
; C:\Python24\python.exe setup.py
; Then drag bibledave.nsi into the MakeNSIS window to compile the installer.

!define PRODUCT_NAME "Bible Dave"
!define PRODUCT_EXE_NAME "bibledave"
!define PRODUCT_VERSION "0.8"
!define PRODUCT_PUBLISHER "Christian Coders Network"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "bibledave-windows32-${PRODUCT_VERSION}.exe"
SetCompressor lzma

LoadLanguageFile "${NSISDIR}\Contrib\Language files\English.nlf"
; LoadLanguageFile "${NSISDIR}\Contrib\Language files\Finnish.nlf"
InstallDir "$PROGRAMFILES\${PRODUCT_NAME}"
Icon "bibledave.ico"
UninstallIcon "bibledave.ico"
DirText "Setup will install $(^Name) in the following folder.$\r$\n$\r$\nTo install in a different folder, click Browse and select another folder."
LicenseText "If you accept all the terms of the agreement, choose I Agree to continue. You must accept the agreement to install $(^Name)."
LicenseData "GPL-License.txt"
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection"
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  ClearErrors

  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\main.exe"
  CreateShortCut "$DESKTOP\${PRODUCT_NAME}.lnk" "$INSTDIR\main.exe"
  
; this used to have quotes around first exe name but it gave compiling error saying that they should be removed (NSIS v2.17) - Jari
;  File "\oname=${PRODUCT_EXE_NAME).exe" "dist\main.exe"
  File "dist\main.exe" 
  File "dist\*.dll"
  File "dist\library.zip"
  File "dist\w9xpopen.exe"
;  File "dist\*.py"
  File "dist\**.ttf"
  File "dist\**.txt"
;  File "dist\**.py"
  SetOutPath "$INSTDIR\enemies"
  File "dist\enemies\*.py"
  SetOutPath "$INSTDIR\images"
  File "dist\images\*.png"
  File "dist\images\*.gif"
  SetOutPath "$INSTDIR\levels"
  File "levels\*.py"
  File "dist\levels\*.lev"
  File "dist\levels\*.tga"
  File "dist\levels\*.png"
  File "dist\levels\*.py"
  SetOutPath "$INSTDIR\levels\tilesets"
  File "dist\levels\tilesets\*.py"
  File "dist\levels\tilesets\*.png"
  SetOutPath "$INSTDIR\locales"
  File "dist\locales\*.pot"
  File "dist\locales\*.bat"
  SetOutPath "$INSTDIR\locales\en\LC_MESSAGES"
  File "dist\locales\en\LC_MESSAGES\*.mo"
  File "dist\locales\en\LC_MESSAGES\*.po"
  SetOutPath "$INSTDIR\locales\fi\LC_MESSAGES"
  File "dist\locales\fi\LC_MESSAGES\*.mo"
  File "dist\locales\fi\LC_MESSAGES\*.po"
  SetOutPath "$INSTDIR\pgu"
  File "dist\pgu\*.py"
  SetOutPath "$INSTDIR\pgu\gui"
  File "dist\pgu\gui\*.py"
  SetOutPath "$INSTDIR\pgu\gui\default"
  File "dist\pgu\gui\default\*.png"
  File "dist\pgu\gui\default\*.xcf"
  File "dist\pgu\gui\default\*.tga"
  File "dist\pgu\gui\default\*.txt"
  SetOutPath "$INSTDIR\sounds"
  File "dist\sounds\*.ogg"
SectionEnd

Section -AdditionalIcons
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall ${PRODUCT_NAME}.lnk" "$INSTDIR\uninst-${PRODUCT_EXE_NAME}.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst-${PRODUCT_EXE_NAME}.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst-${PRODUCT_EXE_NAME}.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\${PRODUCT_EXE_NAME}.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function .onInit
; Make sure that the installer only runs one instance:
  System::Call "kernel32::CreateMutexA(i 0, i 0, t '$(^Name)') i .r0 ?e"
  Pop $0
  StrCmp $0 0 launch
    StrLen $0 "$(^Name)"
    IntOp $0 $0 + 1
  loop:
    FindWindow $1 '#32770' '' 0 $1
    IntCmp $1 0 +4
    System::Call "user32::GetWindowText(i r1, t .r2, i r0) i."
    StrCmp $2 "$(^Name)" 0 loop
    System::Call "user32::SetForegroundWindow(i r1) i."
    Abort
  launch:
; End single instance check
FunctionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\images\*"
  Delete "$INSTDIR\enemies\*"
  Delete "$INSTDIR\pgu\*"
	  Delete "$INSTDIR\pgu\gui\*"
	  Delete "$INSTDIR\pgu\gui\default\*"
  Delete "$INSTDIR\levels\*"
	Delete "$INSTDIR\levels\tilesets\*"
  Delete "$INSTDIR\locales\*"
	Delete "$INSTDIR\locales\en\*"
	  	Delete "$INSTDIR\locales\en\LC_MESSAGES\*"
	Delete "$INSTDIR\locales\fi\*"
	  	Delete "$INSTDIR\locales\fi\LC_MESSAGES\*"
  Delete "$INSTDIR\sounds\*"
  Delete "$INSTDIR\*"
  
  RMDir  "$INSTDIR\images"
  RMDir  "$INSTDIR\enemies"
  RMDir  "$INSTDIR\pgu\gui\default"
  RMDir  "$INSTDIR\pgu\gui"
  RMDir  "$INSTDIR\pgu"
  RMDir  "$INSTDIR\levels\tilesets"
  RMDir  "$INSTDIR\levels"
  RMDir  "$INSTDIR\locales\en\LC_MESSAGES"
  RMDir  "$INSTDIR\locales\en\*"
  RMDir  "$INSTDIR\locales\fi\LC_MESSAGES"
  RMDir  "$INSTDIR\locales\fi"
  RMDir  "$INSTDIR\locales"
  RMDir  "$INSTDIR\sounds"
  RMDir  "$INSTDIR"

  Delete "$DESKTOP\${PRODUCT_NAME}.lnk"
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"
  Delete "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall ${PRODUCT_NAME}.lnk"
  RMDir  "$SMPROGRAMS\${PRODUCT_NAME}"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd