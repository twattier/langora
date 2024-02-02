import { styled } from '@mui/system'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'
import Link from '@mui/material/Link'

import { ContentBox } from '../../utils/style/component'
import LogoGitHub from '../../assets/github-mark.png'
import ChatIcon from '@mui/icons-material/Chat';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';

const MenuButton = styled(Button)(({ theme }) => ({
  backgroundColor: theme.palette.primary.main,
  '&:hover': {
    backgroundColor: theme.palette.secondary.light,
  },
  border: 1,
  borderColor: theme.palette.secondary.main,
  borderRadius: 8,
  color: '#fff',
  // width: '120px',
}))

const MenuIconButton = styled(IconButton)(({ theme }) => ({
  '&:hover': {
    backgroundColor: theme.palette.secondary.light,
  },
}))

export default function Menu() {
  return (
    <ContentBox display="flex" sx={{ pl: 4, pt: 1, pb: 1, mt: 1, mb: 1 }}>
      <Stack
        direction="row"
        width="100%"
        spacing={2}
        justifyContent="flex-start"
      >
        <MenuButton startIcon={<ChatIcon />} href="/">
          Ask
        </MenuButton>
        <MenuButton startIcon={<AutoStoriesIcon />} href="/knowledges">
          Knowledges
        </MenuButton>        
      </Stack>
      <Stack direction="row" alignItems="center" sx={{ mr: 4 }}>
        <Link
          href="https://github.com/twattier/langora"
          target="_blank"
          underline="none"
        >
          <MenuIconButton sx={{ p: 0 }}>
            <img src={LogoGitHub} alt="GitHub" height="30px" />
          </MenuIconButton>
        </Link>
      </Stack>
    </ContentBox>
  )
}
