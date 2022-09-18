import axiosInstance from "@/store/services/axiosInstance";
import tokenStore from "@/store/modules/token";
import axios, { AxiosRequestConfig } from "axios";

function setup(store: any){
  axiosInstance.interceptors.request.use(
    (config) =>{
      const token = tokenStore.access;
      if ( token ){
        config.headers['Authorization'] = 'Bearer ' + token;
      }
      return config
    },
    (error => {
      return Promise.reject(error);
    })
  );
  axiosInstance.interceptors.response.use(
    (res) =>{
      return res;
    },
    async (err) => {
      const originalConfig = err.config;
      if ( originalConfig.url !== tokenStore.OBTAIN_TOKEN_URL && err.response ){
        if ( err.response.status === 401 && !originalConfig._retry) {
          originalConfig._retry = true;
          try {
            const rs = await axiosInstance.post(tokenStore.REFRESH_TOKEN_URL, tokenStore.refresh);
            const accessToken = rs.data;
            tokenStore.setAccess(accessToken);
            return axiosInstance(originalConfig);
          } catch (_error){
            return Promise.reject(_error);
          }
        }
      }
      return Promise.reject(err);
    }
  );
};

export default setup;
