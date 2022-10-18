import React, { useState } from 'react'
import PropTypes from 'prop-types'
import {
  PageHeader, Tag, Row, Statistic, Divider, Card, Button, List, Switch,
} from 'antd'
import { DeleteFilled, PlusOutlined } from '@ant-design/icons';
import { connect, routerRedux } from 'dva'
import { Link } from 'umi'
import PageHeaderLayout from 'layouts/PageHeaderLayout'
import ProjectSelecter from './ProjectSelecter.js'
import TestReportList from './TestReportList'
import styles from './index.less'
import { query } from 'utils/service'
import { api } from 'config'


const Usercenter = ({ usercenter, dispatch, loading }) => {
  const { editmode, pagination, user_info, report_list, modalVisible, modalType } = usercenter
  // get informations from request data: user_info
  console.log(user_info, report_list)
  let username = localStorage.username
  let activity = false
  let last_login = ""
  let preferred_projects = []
  let ProjectTypes = []
  let ProjectObjs = {}
  let total_reports = pagination.total
  if (user_info !== undefined && Object.keys(user_info).length > 0){
    username = user_info.username
    last_login = user_info.last_login
    activity = user_info.is_active
    if (user_info.report_projects && user_info.report_projects.data !== undefined ) {
      user_info.report_projects.data.map(d => {
        ProjectTypes.push(d.type_name)
        ProjectObjs[d.type_name] = {}
        d.content.map(c => {
          //ProjectObjs[d.type_name].push(c.project_name)
          //ProjectObjs[d.type_name].push(c)
          ProjectObjs[d.type_name][c.project_name] = c
        })
      })
      //pick up the projects user prefered from all projects
      if (user_info.preferred_projects !== null && user_info.preferred_projects !== undefined) {
        user_info.preferred_projects.map(p => {
          preferred_projects.push(ProjectObjs[p[0]][p[1]])
        })
      }
    }
  }

  const projectProps = {
    item: {},
    open: modalVisible,
    ProjectTypes: ProjectTypes,
    ProjectObjs: ProjectObjs,
    maskClosable: false,
    confirmLoading: loading.effects['usercenter/query'],
    title: "Add project:",
    wrapClassName: 'vertical-center-modal',
    onOk (data) {
      dispatch({
        type: `usercenter/${modalType}`,
        payload: data,
      })
    },
    onCancel () {
      dispatch({
        type: 'usercenter/hideModal',
      })
    },
  }

  function addProjects(){
    dispatch({
      type: 'usercenter/showModal',
      payload: {
        modalType: 'update',
      },
    })
  }
  function editProjects(checked){
    dispatch({
      type: `usercenter/updateSingleState`,
      payload: { editmode: checked }
    })
  }
  function deleteProjects(item){
    dispatch({
      type: 'usercenter/delete',
      payload: item,
    })
  }

  const reportListProps = {
    dataSource: report_list,
    loading: loading.effects['usercenter/query'],
    pagination,
    location,
    onChange (page) {
      const { query, pathname } = location
      dispatch(routerRedux.push({
        pathname,
        query: {
          ...query,
          page: page.current,
          pageSize: page.pageSize,
        },
      }))
    },
    onDeleteItem (id) {
    },
    onEditItem (item) {
      console.log("you want update item: ", item)
    },
  }

  return (
    <div>
      <PageHeader
        title={ username }
        className="site-page-header"
        subTitle={`Welcom! Last login ${last_login}`}
        tags={activity ? <Tag color="blue">Active</Tag> : <Tag color="yellow">inActive</Tag> }
        avatar={{ src: 'https://avatars1.githubusercontent.com/u/8186664?s=460&v=4' }}
      >
        <Row>
        <Statistic
            title="Projects"
            prefix=""
            value={ preferred_projects.length }
            style={{
              margin: '0 32px',
            }}
          />
          <Statistic
            title="Reports"
            prefix=""
            value={ total_reports }
            style={{
              margin: '0 32px',
            }}
          />
          <Statistic title="Server" prefix="" value={ 0 } />
        </Row>
      </PageHeader>
      <Divider />
      <Card title="My projects" extra={ <Switch checkedChildren="Quit" unCheckedChildren="Edit" defaultChecked={ false } onChange={ (checked) => editProjects(checked) }/> }>
        {preferred_projects.map((item, index) =>
          <Card.Grid style={{ width: '33.3%' }} key={index}>
            <List.Item>
            <List.Item.Meta
              title={<Link to={`/testcenter/testreport?project_name=${item.project_name}&type=${item.type_id}`}>{ item.project_name }</Link>}
              description={`project type: ${item.type_name }, total: ${item.total}, last: ${item.last_run}`}
            />
            <Button type="link" onClick={ () => deleteProjects(item) } hidden={ !editmode }>
              <DeleteFilled />
            </Button>
          </List.Item>
          </Card.Grid>
        )}
        <Card.Grid className={styles.card}>
          <Button type="link" onClick={() => addProjects()} icon={<PlusOutlined />}>
            Add
          </Button>
        </Card.Grid>
      </Card>
      {modalVisible && <ProjectSelecter {...projectProps} />}
      <Divider />
      <Card title="My Report">
        <TestReportList {...reportListProps} />
      </Card>
  </div>
  )
}
Usercenter.propTypes = {
  loading: PropTypes.object,
}

export default connect(({ usercenter, loading }) => ({ usercenter, loading }))(Usercenter)
