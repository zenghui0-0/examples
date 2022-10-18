import React from 'react'
import PropTypes from 'prop-types'
import { Table, Modal, Tag, Menu, Dropdown, Button, Steps } from 'antd'
import { DownOutlined, BarsOutlined } from '@ant-design/icons';
import classnames from 'classnames'
import { DropOption } from 'components'
import { Link } from 'react-router-dom'
import queryString from 'query-string'
import styles from './List.less'
import config from 'utils/config'

const { Step } = Steps

const TestReportList = ({
    onDeleteItem, onEditItem, location, ...tableProps
  }) => {
    location.query = queryString.parse(location.search)
    const handleMenuClick = (record, e) => {
        if (e.key === '1') {
          onEditItem(record)
        } else if (e.key === '2') {
          confirm({
            title: 'Are you sure delete this record?',
            onOk () {
              onDeleteItem(record.id)
            },
          })
        }
    }
    const columns = [
        {
          title: 'id',
          width: 130,
          dataIndex: 'id',
          key: 'id',
          fixed: 'left',
          render: (text, record) => <Link to={`/testcenter/testreport/${record.id}`} style={{ textDecoration: 'underline' }}>{text}</Link>,
        },{
          title: 'Date',
          width: 90,
          dataIndex: 'create_time',
          key: 'create_time',
          fixed: 'left',
          render: (text, record) => <a>{text.split(' ')[0]}</a>,
        }, {
          title: 'Type',
          width: 110,
          dataIndex: 'type_name',
          key: 'type_name',
          render: (text, record) => {
            return <span><Tag color="blue">{text}</Tag></span>
          }
        }, {
          title: 'Project Name',
          width: 200,
          dataIndex: 'project_name',
          key: 'project_name',
        }, {
            title: 'Comments',
            dataIndex: 'comment',
            key: 'comment',
            width: 200,
            render: (text, record) => {
              return text && text !== "" ? text.map(d=> <span>{d}<br/></span>) : <span></span>
            }
        }, {
          title: 'Status Step',
          dataIndex: 'run_step',
          key: 'run_step',
          render: (text, record) => {
            let run_type = {}
            config.testreport_run_type.map(d => {
              if (d.keyword === text){
                run_type = d
              }
            })
            if (record.run_status){
              return (
                <Steps size="small">
                  <Step status={"process"} icon={<LoadingOutlined/>} key={run_type.keyword} title={run_type.name}/>
                </Steps>
              )
            }else{
              if (run_type.keyword == 4){
                return (
                  <Steps size="small">
                    <Step status={"finish"} key={run_type.keyword} title={run_type.name}/>
                  </Steps>
                )
              } else {
                return (
                  <Steps size="small">
                    <Step status={"error"} key={run_type.keyword} title={run_type.name}/>
                  </Steps>
                )
              }
            }
          }
        }, {
          title: 'Requester',
          dataIndex: 'requester',
          key: 'requester',
          render: (text, record) => {
            return <span><Tag color="blue">{text}</Tag></span>
          }
        }, {
            title: 'Action',
            key: 'operation',
            render: (text, record) => {
              return <DropOption onMenuClick={e => handleMenuClick(record, e)} menuOptions={[{ key: '1', name: 'Update' }]} />
            },
        },
      ]

  return (<div>
            <Table
              {...tableProps}
              className={classnames({ [styles.table]: true })}
              bordered
              columns={columns}
              simple
              rowKey={record => record.id}
              size="small"
              sticky
            />
          </div>
  )
}
TestReportList.proptypes = {
    onDeleteItem: PropTypes.func,
    onEditItem: PropTypes.func,
    location: PropTypes.object,
  }
  
export default TestReportList
