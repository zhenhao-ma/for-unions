import { get, post, put } from "./base";

function UserCreate (data: IUnionCreate): Promise<IUnion> {
  return post<IUnion>("/union/user/create", data)
}

function UserUpdate (id: string, data: IUnionUpdate): Promise<IUnion> {
  return put<IUnion>(`/union/user/update/${id}`, data)
}

function UserApply (data: IApplyCreate): Promise<IApply> {
  return post<IApply>("/union/user/apply", data)
}
function UserReview (data: IApplyReview): Promise<IApply> {
  return post<IApply>("/union/user/review", data)
}
function UserList (data: {skip: number, limit: number}): Promise<IUnion[]> {
  return get<IUnion[]>("/union/user/list", data)
}
function UserListApply (data: {skip: number, limit: number}): Promise<IApply[]> {
  return get<IApply[]>("/union/user/list/apply", data)
}
function PublicGet (data: {id: string}): Promise<IUnion> {
  return get<IUnion>("/union/public/obj", data)
}

export const UNION_API = {
  UserCreate,
  UserApply,
  UserReview,
  UserList,
  PublicGet,
  UserListApply,
  UserUpdate
}