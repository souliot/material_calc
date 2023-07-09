export interface BasicPageParams {
  page: number;
  pageSize: number;
}

export interface BasicApiResponse<T extends any> {
  version: string;
  message: string;
  timestamp: GLint64;
  code: GLint64;
  result: boolean;
  data?: T;
}

export interface BasicApiListResponse<T extends any> {
  version: string;
  message: string;
  timestamp: GLint64;
  code: GLint64;
  result: boolean;
  data?: BasicApiListModel<T>;
}

export interface BasicApiListModel<T extends any> {
  items: T[];
  total: GLint64;
}
