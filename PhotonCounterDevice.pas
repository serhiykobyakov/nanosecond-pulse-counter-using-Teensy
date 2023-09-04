unit PhotonCounterDevice;
{
PhotonCounter unit
Version 04.10.2023

(c) Serhiy Kobyakov
}

interface

uses
  Classes, SysUtils, dialogs, StdCtrls, Controls, Forms,
//  strutils,
  //Math,
  IniFiles,
  addfunc,
  ArduinoDevice;


type
  { PhotonCounter_device }
  PhotonCounter_device = Object (_ArduinoDevice)
    private
      fExpo: Real;
      fExpoStr: string;

    public
      constructor Init(_ComPort: string);
      destructor Done;

      function SetExpo(newexpo: string): string;
      function GetCPS(): Real;

  end;


implementation


constructor PhotonCounter_device.Init(_ComPort: string);
var
  MyForm: TForm;
  MyLabel: TLabel;
  UpperInitStr, iniFile: string;
  AppIni: TIniFile;
begin
// -----------------------------------------------------------------------------
// first things first
// the device ID string with which it responds to '?'
  theDeviceID := 'PhotonCounter';
// -----------------------------------------------------------------------------

  iniFile := Application.Location + theDeviceID + '.ini';
  If not FileExists(iniFile) then
    begin
      showmessage(theDeviceID + ':' + LineEnding +
          'procedure ''' + {$I %CURRENTROUTINE%} + ''' failed!' + LineEnding +
          'File ' + iniFile + 'has not been found!' + LineEnding +
          'Please fix it');
      halt(0);
    end;

// make a splash screen
// which shows initialization process
  MyForm := TForm.Create(nil);
  with MyForm do begin
     Caption := theDeviceID + ' initialization...';
     SetBounds(0, 0, 450, 90); Position:=poDesktopCenter; BorderStyle := bsNone;
     MyForm.Color := $00EEEEEE; end;

  MyLabel := TLabel.Create(MyForm);
  with MyLabel do begin
     Autosize := True; Align := alNone; Alignment := taCenter; Parent := MyForm;
     Visible := True; AnchorVerticalCenterTo(MyForm);
     AnchorHorizontalCenterTo(MyForm); end;
  UpperInitStr := 'Initializing ' + theDeviceID + ':' + LineEnding;

  MyForm.Show; MyForm.BringToFront;
  UpperInitStr := 'Initializing ' + theDeviceID + ':' + LineEnding;

  MyLabel.Caption:= UpperInitStr + 'Reading ' + theDeviceID + '.ini...';
  sleepFor(50); // refresh the Label to see the change

// -----------------------------------------------------------------------------
// Read the device variables from ini file:
//  AppIni := TInifile.Create(iniFile);

//  AppIni.Free;


// basic device initialization
  MyLabel.Caption:= UpperInitStr + 'Connecting to ' + _ComPort + '...';
  sleepFor(200); // refresh the Label to see the change
  Inherited Init(_ComPort);

// read actual exposition value
  MyLabel.Caption:= UpperInitStr + 'Reading exposition value...';
  sleepFor(300); // refresh the Label to see the change
  fExpoStr := Trim(SendAndGetAnswer('e'));
  fExpo := StrToFloat(fExpoStr);
  theLongReadTimeout := Round(2 * 2700 + 1000 * fExpo);

  MyLabel.Caption:= UpperInitStr + 'Done!';
  sleepFor(300); // refresh the Label just to see "Done"

  MyForm.Close;
  FreeAndNil(MyForm);
end;


destructor PhotonCounter_device.Done;
begin
  Inherited Done;
end;


function PhotonCounter_device.SetExpo(newexpo: string): string;
// set exposition value
var
  answer: string;
begin
  answer := Trim(SendAndGetAnswer('e' + newexpo));
  fExpo := Str2Float(answer);
  theLongReadTimeout := Round(2 * 2700 + 1000 * fExpo);
  Result := answer;
end;


function PhotonCounter_device.GetCPS: Real;
// get actual counts per second reading
var
  answer: string;
begin
  answer := Trim(SendAndGetAnswer('r'));
  Result := Str2Float(answer);
end;


end.


