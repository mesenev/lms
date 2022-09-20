import {AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse} from "axios";
import tokenStore from '@/store/modules/token'

const onRequest = (config: AxiosRequestConfig): AxiosRequestConfig => {
    const access = tokenStore.access;
    config.headers['Authorization'] = 'Bearer ' + access;
    return config;
}

const onRequestError = (error: AxiosError): Promise<AxiosError> => {
    return Promise.reject(error);
}

function setupInterceptorsTo(axiosInstance: AxiosInstance): AxiosInstance {
    axiosInstance.interceptors.request.use(onRequest, onRequestError);
    axiosInstance.interceptors.response.use(
      (res) => {return res},
      async (err) => {
        if ( err.config.url !== tokenStore.OBTAIN_TOKEN_URL && err.response ){
          if ( err.response.status === 401 ){
            try {
              const rs = await axiosInstance.post(tokenStore.REFRESH_TOKEN_URL, tokenStore.refresh);
              const accessToken = rs.data;
              tokenStore.setAccess(accessToken);
            }catch (error){
              console.log(error);
            }
          }
        }
      }
    );
    return axiosInstance;
}

export default setupInterceptorsTo;
