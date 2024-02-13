import * as React from 'react'
import { styled } from '@mui/system'
import { useTheme } from '@mui/material/styles'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'
import ListItemText from '@mui/material/ListItemText'
import CircularProgress from '@mui/material/CircularProgress'
import AddIcon from '@mui/icons-material/Add'
import TopicIcon from '@mui/icons-material/Topic'

import { ContentBox, ContentBoxTitle } from '../../utils/style/component'
import NavBar from '../../components/App/NavBar'
import AddTopic from '../../components/Knowledges/AddTopic'
import ListSearches from '../../components/Atoms/ListSearches'

import { useFetchTopics } from '../../utils/hooks'

export default function Topics() {
  const { topics, isLoadingTopics, errorLoadingTopics } = useFetchTopics()

  const [selectedTopic, setSelectedTopic] = React.useState()
  const handleListItemClick = (event, id) => {
    setSelectedTopic(id)
  }

  const theme = useTheme()

  if (errorLoadingTopics) {
    return <span>Impossible to load the liste of Tasks</span>
  }

  return (
    <Stack sx={{ ml: 1 }}>
      <NavBar selected="topics" />

      {isLoadingTopics ? (
        <CircularProgress />
      ) : (
        <Stack direction="row" spacing={1}>
          <ContentBox sx={{ ml: 1, width: '30%' }}>
            <List>
              <ListItemButton
                onClick={(event) => handleListItemClick(event, undefined)}
              >
                <ContentBoxTitle>
                  <AddIcon
                    sx={{
                      border: 1,
                      borderRadius: 8,
                      mr: 1,
                    }}
                  />
                  Topics
                </ContentBoxTitle>
              </ListItemButton>
            </List>
            <Divider />
            <List dense>
              {topics?.map((topic) => (
                <ListItemButton
                  selected={selectedTopic?.id === topic.id}
                  onClick={(event) => handleListItemClick(event, topic)}
                >
                  <TopicIcon sx={{ mr: 1 }} />
                  {topic.name}
                </ListItemButton>
              ))}
            </List>
          </ContentBox>
          <ContentBox sx={{ width: '70%' }}>
            {selectedTopic === undefined ? (
              <AddTopic />
            ) : (
              <Box>
                <List>
                  <ListItemButton>
                    <ContentBoxTitle>
                      <TopicIcon sx={{ mr: 1 }} />
                      {selectedTopic.name}
                    </ContentBoxTitle>
                  </ListItemButton>
                </List>
                <Divider />
                <ListSearches searches={selectedTopic.searches} />
              </Box>
            )}
          </ContentBox>
        </Stack>
      )}
    </Stack>
  )
}
