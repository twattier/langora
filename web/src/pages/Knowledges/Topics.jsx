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
import SearchIcon from '@mui/icons-material/Search'

import { ContentBox } from '../../utils/style/component'
import NavBar from '../../components/Knowledges/NavBar'
import AddTopic from '../../components/Knowledges/AddTopic'

import { useFetchTopics } from '../../utils/hooks'

export default function Topics() {
  const { topics, isLoadingTopics, errorLoadingTopics } = useFetchTopics()

  const [selectedTopic, setSelectedTopic] = React.useState()
  const handleListItemClick = (event, id) => {
    setSelectedTopic(id)
  }

  const theme = useTheme()
  const ListTopicButton = styled(ListItemButton)(({ theme }) => ({
    '& .MuiListItemButton-root': {
      '&.Mui-selected': {
        color: theme.palette.secondary.main,
      },
    },
  }))

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
              <ListTopicButton
                onClick={(event) => handleListItemClick(event, undefined)}
              >
                <AddIcon
                  sx={{
                    border: 1,
                    borderRadius: 8,
                    mr: 2,
                    color: theme.palette.primary.main,
                  }}
                />
                <ListItemText
                  primary="Topics"
                  primaryTypographyProps={{
                    color: theme.palette.primary.main,
                    fontWeight: 'bold',
                  }}
                />
              </ListTopicButton>
            </List>
            <Divider />
            <List dense>
              {topics?.map((topic) => (
                <ListTopicButton
                  selected={selectedTopic?.id === topic.id}
                  onClick={(event) => handleListItemClick(event, topic)}
                >
                  <TopicIcon sx={{ mr: 1 }} />
                  {topic.name}
                </ListTopicButton>
              ))}
            </List>
          </ContentBox>
          <ContentBox sx={{ width: '70%' }}>
            {selectedTopic === undefined ? (
              <AddTopic />
            ) : (
              <Box>
                <List>
                  <ListTopicButton>
                    <Typography
                      variant="subtitle1"
                      align="center"
                      color="primary"
                      sx={{ fontWeight: 'bold' }}
                    >
                      <TopicIcon sx={{ mr: 1 }} />
                      {selectedTopic.name}
                    </Typography>
                  </ListTopicButton>
                </List>
                <Divider />
                <List dense>
                  {selectedTopic.searches?.map((search) => (
                    <ListTopicButton>
                      <Typography variant="body2">
                        <SearchIcon sx={{ mr: 1 }} />
                        {`${search.query} [${search.nb_sources}]`}
                      </Typography>
                    </ListTopicButton>
                  ))}
                </List>
              </Box>
            )}
          </ContentBox>
        </Stack>
      )}
    </Stack>
  )
}
