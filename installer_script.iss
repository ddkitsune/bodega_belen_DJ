; Script de Inno Setup para Bodega de Belén
; Crea un instalador profesional de Windows

[Setup]
AppName=Bodega de Belén
AppVersion=1.0
AppPublisher=Bodega de Belén
DefaultDirName={autopf}\BodegaBelen
DefaultGroupName=Bodega de Belén
OutputDir=Output
OutputBaseFilename=Setup_BodegaBelen
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Accesos directos:"

[Files]
; Copiar todos los archivos del proyecto
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Excluir archivos innecesarios
Source: "*"; Excludes: "venv\*,__pycache__\*,*.pyc,*.pyo,.git\*,.env"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Bodega de Belén"; Filename: "{app}\INICIAR_BODEGA.bat"
Name: "{autodesktop}\Bodega de Belén"; Filename: "{app}\INICIAR_BODEGA.bat"; Tasks: desktopicon

[Run]
Filename: "{app}\INICIAR_BODEGA.bat"; Description: "Iniciar Bodega de Belén"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  // Verificar si Python está instalado
  if not FileExists(ExpandConstant('{sys}\python.exe')) and 
     not FileExists(ExpandConstant('{pf}\Python*\python.exe')) then
  begin
    MsgBox('Python no está instalado. Por favor instala Python 3.11 o superior antes de continuar.', mbError, MB_OK);
    Result := False;
  end
  else
    Result := True;
end;
