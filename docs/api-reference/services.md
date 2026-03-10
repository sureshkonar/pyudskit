# Services (Offline)

Each UDS service is implemented as a class in `pyudskit.services`. Every class can:

- `build_request(...)`
- `parse_response(...)`
- `validate(...)`

## Session Management

- `DiagnosticSessionControl`
- `ECUReset`
- `SecurityAccess`
- `CommunicationControl`
- `Authentication`
- `TesterPresent`
- `AccessTimingParameter`
- `SecuredDataTransmission`
- `ControlDTCSetting`
- `ResponseOnEvent`
- `LinkControl`

## Data Transmission

- `ReadDataByIdentifier`
- `ReadMemoryByAddress`
- `ReadScalingDataByIdentifier`
- `ReadDataByPeriodicIdentifier`
- `DynamicallyDefineDataIdentifier`
- `WriteDataByIdentifier`
- `WriteMemoryByAddress`

## DTC Management

- `ClearDiagnosticInformation`
- `ReadDTCInformation`

## I/O Control

- `InputOutputControlByIdentifier`

## Routine Control

- `RoutineControl`

## Upload / Download

- `RequestDownload`
- `RequestUpload`
- `TransferData`
- `RequestTransferExit`
- `RequestFileTransfer`

## API Docs

::: pyudskit.services

::: pyudskit.services.session_management.diagnostic_session_control.DiagnosticSessionControl
::: pyudskit.services.session_management.ecu_reset.ECUReset
::: pyudskit.services.session_management.security_access.SecurityAccess
::: pyudskit.services.session_management.communication_control.CommunicationControl
::: pyudskit.services.session_management.authentication.Authentication
::: pyudskit.services.session_management.tester_present.TesterPresent
::: pyudskit.services.session_management.access_timing_parameter.AccessTimingParameter
::: pyudskit.services.session_management.secured_data_transmission.SecuredDataTransmission
::: pyudskit.services.session_management.control_dtc_setting.ControlDTCSetting
::: pyudskit.services.session_management.response_on_event.ResponseOnEvent
::: pyudskit.services.session_management.link_control.LinkControl

::: pyudskit.services.data_transmission.read_data_by_identifier.ReadDataByIdentifier
::: pyudskit.services.data_transmission.read_memory_by_address.ReadMemoryByAddress
::: pyudskit.services.data_transmission.read_scaling_data.ReadScalingDataByIdentifier
::: pyudskit.services.data_transmission.read_data_by_periodic_id.ReadDataByPeriodicIdentifier
::: pyudskit.services.data_transmission.dynamically_define_did.DynamicallyDefineDataIdentifier
::: pyudskit.services.data_transmission.write_data_by_identifier.WriteDataByIdentifier
::: pyudskit.services.data_transmission.write_memory_by_address.WriteMemoryByAddress

::: pyudskit.services.dtc_management.clear_diagnostic_info.ClearDiagnosticInformation
::: pyudskit.services.dtc_management.read_dtc_information.ReadDTCInformation

::: pyudskit.services.io_control.input_output_control.InputOutputControlByIdentifier

::: pyudskit.services.routine_control.routine_control.RoutineControl

::: pyudskit.services.upload_download.request_download.RequestDownload
::: pyudskit.services.upload_download.request_upload.RequestUpload
::: pyudskit.services.upload_download.transfer_data.TransferData
::: pyudskit.services.upload_download.request_transfer_exit.RequestTransferExit
::: pyudskit.services.upload_download.request_file_transfer.RequestFileTransfer
