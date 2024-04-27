import { get, put } from "./base";

function PublicWeminiGetPhone (wx_code: string): Promise<IWechatPhoneInfoPublic> {
  return get<IWechatPhoneInfoPublic>("/user/public/wemini/get_phone", {wx_code})
}
export type IPublicWeminiLogin = {
  js_code: string
  phone: Phone
  secret: string
}
function PublicWeminiLogin (data: IPublicWeminiLogin): Promise<IToken> {
  return get<IToken>("/user/public/wemini/login", data)
}
function UserGetSelf (): Promise<IUserDetailed> {
  return get<IUserDetailed>("/user/user")
}
function UserUpdate (data: IUserUpdate): Promise<IUserDetailed> {
  return put<IUserDetailed>("/user/user", data)
}
function PublicList (data?: { union_id: string, skip: number, limit: number }): Promise<IUserPreview[]> {
  return get<IUserPreview[]>("/user/public/list", data || {})
}
export const USER_API = {
  PublicWeminiGetPhone,
  PublicWeminiLogin,
  UserUpdate,
  PublicList,
  UserGetSelf
}