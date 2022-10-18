import { Select, Form, Modal, message  } from 'antd';
import React, { useState } from 'react';
import PropTypes from 'prop-types'

const { Option } = Select;
/*
const ProjectTypes = ['Zhejiang', 'Jiangsu', 'Jiangxi'];
const ProjectObjs = {
  Zhejiang: ['Hangzhou', 'Ningbo', 'Wenzhou'],
  Jiangsu: ['Nanjing', 'Suzhou', 'Zhenjiang'],
  Jiangxi: [],
};
*/
const FormItem = Form.Item

const formItemLayout = {
  labelCol: {
    span: 6,
  },
  wrapperCol: {
    span: 14,
  },
}

const ProjectSelecter = ({
  onOk,
  ...projectProps
}) => {
  const { ProjectTypes, ProjectObjs } = projectProps
  if (ProjectTypes.length === 0 || ProjectObjs[ProjectTypes[0]].length === 0) {
    message.success('All projects is loading, please wait a second...', 3)
    return( <p></p> )
  }

  const formRef = React.createRef()
  const first_type = ProjectTypes[0]
  const first_name = Object.keys(ProjectObjs[first_type])[0]
  const [projectName, setProjectName] = useState(first_name);
  const [projectNames, setProjectNames] = useState(Object.keys(ProjectObjs[first_type]));

  const handleTypeChange = (value) => {
    setProjectNames(Object.keys(ProjectObjs[value]));
    setProjectName(Object.keys(ProjectObjs[value])[0]);
    formRef.current.setFieldsValue({
        project_type: value,
        project_name: Object.keys(ProjectObjs[value])[0],
    })
  };

  const handleNameChange = (value) => {
    setProjectName(value);
  };

  const handleOk = () => {
    formRef.current.validateFields()
      .then(values => {
        const data = {
          ...values,
        }
        onOk(data)
      })
      .catch(errorInfo => {
        console.log(errorInfo)
      })
  }
  const modalOpts = {
    ...projectProps,
    onOk: handleOk,
  }

  return (
    <Modal {...modalOpts}>
      <Form ref={formRef} initialValues={{ project_type: first_type, project_name: first_name }}>
        <FormItem label="Project Type:" name='project_type' hasFeedback {...formItemLayout} rules={[{ required: true }]}>
          <Select
            style={{
              width: 200,
            }}
            onChange={handleTypeChange}
          >
            {ProjectTypes.map((t) => (
              <Option key={t}>{t}</Option>
            ))}
          </Select>
        </FormItem>
        <FormItem label="Project Name:" name='project_name' hasFeedback {...formItemLayout} rules={[{ required: true }]}>
          <Select
            style={{
              width: 200,
            }}
            value={projectName}
            onChange={handleNameChange}
          >
            {projectNames.map((n) => (
              <Option key={n}>{n}</Option>
            ))}
          </Select>
        </FormItem>
      </Form>
    </Modal>
  );
};

ProjectSelecter.propTypes = {
  onOk: PropTypes.func,
}

export default ProjectSelecter;
