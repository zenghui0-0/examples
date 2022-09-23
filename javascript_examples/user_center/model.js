import modelExtend from 'dva-model-extend'
import { CommonModel } from 'utils/model'
import { api, pageSize } from 'config'
import * as commonService from 'utils/service'

const path = api.users
export default modelExtend(CommonModel(
  '/users/center',
  path,
  ({ usercenter }) => usercenter.currentItem.id
), {
  namespace: 'usercenter',

  state: {
    editmode: false,
  },

  subscriptions: {},

  effects: {
    *query({ payload = {} }, { call, put, select }) {
      const data = yield call(commonService.query, { path, payload });
      if (data.statusCode === 403 && path.indexOf('/plan/report') < 0) {
        yield put(routerRedux.push('/exception/403'));
      } else if (data) {
        yield put({
          type: 'querySuccess',
          payload: {
            // user,
            // windowSize,
            user_info: data.data,
            report_list: data.report_list,
            pagination: {
              current: Number(payload.page) || 1,
              pageSize: Number(payload.pageSize) || pageSize,
              total: data.total
            }
          }
        });
      }
    },
  },

  reducers: {
    querySuccess(state, { payload }) {
      const { user, windowSize, user_info, report_list, pagination } = payload;
      return {
        ...state,
        user,
        windowSize,
        user_info,
        report_list,
        pagination: {
          ...state.pagination,
          ...pagination
        }
      };
    }
  },

})
