import * as React from 'react'
import { styled } from '@mui/system'

import Tabs from '@mui/material/Tabs'
import Tab from '@mui/material/Tab'

import TopicIcon from '@mui/icons-material/Topic'
import SearchIcon from '@mui/icons-material/Search'
import DescriptionIcon from '@mui/icons-material/Description'
import SystemUpdateAltIcon from '@mui/icons-material/SystemUpdateAlt'

const CustomTab = styled(Tab)(({ theme }) => ({
  fontWeight: 'bold',
}))

export default function NavBar(props) {
  const { selected } = props

  return (
    <Tabs
      value={selected}
      textColor="secondary"
      indicatorColor="secondary"
      sx={{ mb: 1 }}
    >
      <CustomTab
        value="topics"
        icon={<TopicIcon />}
        label="Topics"
        href="/knowledges/topics"
      />
      <CustomTab
        value="searches"
        icon={<SearchIcon />}
        label="Searches"
        href="/knowledges/searches"
      />
      <CustomTab
        value="sources"
        icon={<DescriptionIcon />}
        label="Sources"
        href="/knowledges/sources"
      />
      <CustomTab
        value="tasks"
        icon={<SystemUpdateAltIcon />}
        label="Tasks"
        href="/knowledges/tasks"
      />
    </Tabs>
  )
}
