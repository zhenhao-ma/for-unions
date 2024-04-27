import { post } from "./base";

function UserCreate (data: IConnectCreate): Promise<IConnect> {
  return post<IConnect>("/connect/user/create", data)
}

function UserReview (data: IConnectReview): Promise<IConnect> {
  return post<IConnect>("/connect/user/review", data)
}

export const CONNECT_API = {
  UserCreate,
  UserReview
}