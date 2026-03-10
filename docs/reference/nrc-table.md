# Negative Response Code Table

| NRC | Name | Meaning | Common Cause | Resolution |
|---|---|---|---|---|
| 0x10 | generalReject | ECU rejected request | Generic error | Retry or check service support |
| 0x11 | serviceNotSupported | Service unsupported | ECU does not implement | Use supported service |
| 0x12 | subFunctionNotSupported | Subfunction unsupported | Invalid subfunction | Use valid subfunction |
| 0x13 | incorrectMessageLengthOrInvalidFormat | Bad length/format | Wrong payload length | Fix request format |
| 0x14 | responseTooLong | Response too long | Buffer limits | Use smaller request |
| 0x21 | busyRepeatRequest | ECU busy | ECU overloaded | Wait and retry |
| 0x22 | conditionsNotCorrect | Preconditions not met | Wrong session/state | Switch session or meet conditions |
| 0x23 | requestSequenceError | Invalid sequence | Wrong order | Follow correct flow |
| 0x24 | noResponseFromSubnetComponent | Subnet not responding | Gateway issue | Check subnet device |
| 0x25 | failurePreventsExecutionOfRequestedAction | Internal failure | ECU error | Retry after reset |
| 0x26 | requestCorrectlyReceivedResponsePending | Response pending | Long operation | Wait for final response |
| 0x31 | requestOutOfRange | Parameter out of range | Invalid DID/address | Fix parameters |
| 0x32 | securityAccessDenied | Security denied | Locked ECU | Perform SecurityAccess |
| 0x33 | securityAccessDenied | Security denied | Locked ECU | Perform SecurityAccess |
| 0x34 | authenticationRequired | Authentication required | Missing auth | Run authentication |
| 0x35 | invalidKey | Wrong security key | Bad key algorithm | Recompute key |
| 0x36 | exceedNumberOfAttempts | Too many attempts | Brute force | Wait and retry later |
| 0x37 | requiredTimeDelayNotExpired | Delay not expired | Lockout active | Wait and retry |
| 0x38 | secureDataTransmissionRequired | Secure data needed | Missing secure channel | Enable secure data transmission |
| 0x39 | secureDataTransmissionNotAllowed | Secure data not allowed | Policy restriction | Check ECU policy |
| 0x3A | secureDataVerificationFailed | Verification failed | Bad signature | Verify payload |
| 0x50 | certificateVerificationFailedInvalidTimePeriod | Cert invalid time | Expired cert | Update cert |
| 0x51 | certificateVerificationFailedInvalidSignature | Cert signature invalid | Bad cert | Replace cert |
| 0x52 | certificateVerificationFailedInvalidChainOfTrust | Bad chain | Untrusted CA | Install correct chain |
| 0x53 | certificateVerificationFailedInvalidType | Cert type invalid | Wrong cert type | Use correct cert |
| 0x54 | certificateVerificationFailedInvalidFormat | Cert format invalid | Corrupt cert | Reissue cert |
| 0x55 | certificateVerificationFailedInvalidContent | Cert content invalid | Bad fields | Reissue cert |
| 0x56 | certificateVerificationFailedInvalidScope | Cert scope invalid | Out of scope | Use proper scope |
| 0x57 | certificateVerificationFailedInvalidCertificateName | Cert name invalid | CN mismatch | Use correct cert |
| 0x58 | certificateVerificationFailedInvalidCertificateSecurity | Cert security invalid | Weak security | Use stronger cert |
| 0x59 | certificateVerificationFailedInvalidCertificateData | Cert data invalid | Corrupt data | Reissue cert |
| 0x5A | certificateVerificationFailedInvalidCertificateLength | Cert length invalid | Corrupt length | Reissue cert |
| 0x5B | certificateVerificationFailedInvalidCertificateID | Cert ID invalid | Unknown cert ID | Use correct cert ID |
| 0x5C | certificateVerificationFailedInvalidCertificateRole | Cert role invalid | Wrong role | Use correct role |
| 0x5D | certificateVerificationFailedInvalidCertificateSupplier | Cert supplier invalid | Untrusted supplier | Use trusted supplier |
| 0x70 | uploadDownloadNotAccepted | Upload/download rejected | Wrong session | Switch to programming |
| 0x71 | transferDataSuspended | Transfer suspended | Flow interrupted | Resume transfer |
| 0x72 | generalProgrammingFailure | Programming failed | Flash error | Retry or check memory |
| 0x73 | wrongBlockSequenceCounter | Block counter wrong | Sequence error | Fix counter and retry |
| 0x78 | requestCorrectlyReceivedResponsePending | Response pending | Long operation | Wait for final response |
| 0x7E | subFunctionNotSupportedInActiveSession | Not supported in session | Wrong session | Switch session |
| 0x7F | serviceNotSupportedInActiveSession | Service blocked in session | Wrong session | Switch session |
| 0x81 | rpmTooHigh | RPM too high | Engine state | Adjust RPM |
| 0x82 | rpmTooLow | RPM too low | Engine state | Adjust RPM |
| 0x83 | engineIsRunning | Engine running | Safety rule | Stop engine |
| 0x84 | engineIsNotRunning | Engine not running | Safety rule | Start engine |
| 0x85 | engineRunTimeTooLow | Engine runtime low | Preconditions | Run engine longer |
| 0x86 | temperatureTooHigh | Temperature too high | Safety rule | Cool down |
| 0x87 | temperatureTooLow | Temperature too low | Safety rule | Warm up |
| 0x88 | vehicleSpeedTooHigh | Speed too high | Safety rule | Slow down |
| 0x89 | vehicleSpeedTooLow | Speed too low | Safety rule | Increase speed |
| 0x8A | throttlePedalTooHigh | Throttle too high | Safety rule | Release throttle |
| 0x8B | throttlePedalTooLow | Throttle too low | Safety rule | Press throttle |
| 0x8C | transmissionRangeNotInNeutral | Not in neutral | Safety rule | Shift to neutral |
| 0x8D | transmissionRangeNotInGear | Not in gear | Safety rule | Shift to gear |
| 0x8E | brakeSwitchNotClosed | Brake not pressed | Safety rule | Press brake |
| 0x8F | shifterLeverNotInPark | Not in park | Safety rule | Shift to park |
| 0x90 | torqueConverterClutchLocked | TCC locked | Safety rule | Unlock TCC |
| 0x91 | voltageTooHigh | Voltage high | Electrical state | Stabilize voltage |
| 0x92 | voltageTooLow | Voltage low | Electrical state | Stabilize voltage |
| 0x93 | ecuInCalibrationMode | ECU in calibration mode | State restriction | Exit calibration mode |
| 0x94 | vehicleIsMoving | Vehicle moving | Safety rule | Stop vehicle |
