type Option<T> = {
  id: T
  name: string
}
interface IConfig {
  API_PREFIX: string,
  COUNTRIES: Option<Country>[],
  CONNECT_TYPES: Option<ConnectType>[]
}