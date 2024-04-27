import { get } from "./base";

function Register (phone: Phone): Promise<IToken> {
  return get<IToken>("/dev_only/get_token", {phone})
}
function GenerateRandomApplies (): Promise<IStatus> {
  return get<IStatus>("/dev_only/random_applies")
}

export const DEV_ONLY_API = {
  Register,
  GenerateRandomApplies
}