;-------------------------------------------------------
; Instalador todo en uno para SAFT (Python + Flet)
;-------------------------------------------------------

[Setup]
AppName=SAFT
AppVersion=1.0
DefaultDirName={pf}\SAFT
DefaultGroupName=SAFT
OutputBaseFilename=InstaladorSAFT
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
WizardStyle=modern
Uninstallable=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
; Copiar tu app Flet (reportes_SAFT.exe y carpeta completa)
Source: "AppFlet\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

; Copiar dependencias a carpeta temporal
Source: "Dependencies\vc_redist.x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "Dependencies\sqlncli.msi"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "Dependencies\MicrosoftEdgeWebview2Setup.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
; Crear acceso directo en escritorio (Task lo controla)
Filename: "{app}\reportes_SAFT.exe"; Description: "SAFT"; WorkingDir: "{app}"; IconFilename: "{app}\reportes_SAFT.exe"; Tasks: desktopicon

[Icons]
Name: "{group}\SAFT"; Filename: "{app}\reportes_SAFT.exe"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones"; Flags: unchecked

[Code]
var
  ResultCode: Integer;

//---------------------------------------------------
// Funciones para verificar dependencias
//---------------------------------------------------

function IsVCInstalled(): Boolean;
var
  dummy: string;
begin
  Result := RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Installed', dummy) and (dummy='1');
end;

function IsSQLNativeClientInstalled(): Boolean;
var
  dummy: string;
begin
  Result := RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\Microsoft SQL Server\SQLNCLI10\CurrentVersion', 'CurrentVersion', dummy);
end;

function IsWebView2Installed(): Boolean;
var
  dummy: string;
begin
  Result := RegQueryStringValue(HKLM, 'Software\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', dummy);
end;

//---------------------------------------------------
// Paso después de copiar archivos
//---------------------------------------------------
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Cerrar procesos que bloquean WebView2
    Exec('taskkill.exe','/F /IM msedgewebview2.exe','',SW_HIDE,ewWaitUntilTerminated,ResultCode);
    Exec('taskkill.exe','/F /IM msedge.exe','',SW_HIDE,ewWaitUntilTerminated,ResultCode);

    // Instalar Visual C++ Redistributable si no está
    if not IsVCInstalled() then
      Exec(ExpandConstant('{tmp}\vc_redist.x64.exe'), '/install /quiet /norestart','', SW_HIDE, ewWaitUntilTerminated, ResultCode);

    // Instalar SQL Native Client si no está
    if not IsSQLNativeClientInstalled() then
      Exec('msiexec.exe','/i "' + ExpandConstant('{tmp}\sqlncli.msi') + '" /quiet /norestart','', SW_HIDE, ewWaitUntilTerminated, ResultCode);

    // Instalar WebView2 Runtime si no está
    if not IsWebView2Installed() then
      Exec(ExpandConstant('{tmp}\MicrosoftEdgeWebView2RuntimeInstallerX64.exe'), '/silent /install','', SW_HIDE, ewWaitUntilTerminated, ResultCode);

    // Mensaje final
    if IsWebView2Installed() then
      MsgBox('Instalación completada correctamente. WebView2 está disponible.', mbInformation, MB_OK)
    else
      MsgBox('Instalación completada, pero WebView2 no se pudo verificar.', mbError, MB_OK);
  end;
end;
