import { styled } from '@mui/system'

import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import { Typography } from '@mui/material'

export const ContentBox = styled((props) => <Box {...props} />)(
  ({ theme }) => ({
    backgroundColor: theme.palette.content.main,
    border: '1px solid',
    borderColor: theme.palette.content.dark,
    borderRadius: '4px',
  })
)
export const ContentBoxTitle = styled((props) => (
  <Typography variant="subtitle1" color="primary" {...props} />
  ))
  (({ theme }) => ({
    fontWeight: 'bold',   
    paddingLeft: 16, 
  }))

export const InputText = styled((props) => <TextField {...props} />)(
  ({ theme }) => ({
    '& .MuiFilledInput-root': {
      backgroundColor: 'white',
    },
    '& .MuiOutlinedInput-root': {
      '& fieldset': {
        borderColor: theme.palette.content.dark,
      },
      '&:hover fieldset': {
        borderColor: theme.palette.primary.light,
      },
      '&.Mui-focused fieldset': {
        borderColor: theme.palette.primary.main,
      },
    },
  })
)

export const ButtonGenAI = styled(Button)(({ theme }) => ({
  backgroundColor: theme.palette.secondary.main,
  '&:hover': {
    backgroundColor: theme.palette.secondary.light,
  },
  border: 1,
  borderColor: theme.palette.secondary.dark,
  borderRadius: 8,
  color: '#fff',
}))

export const ActionButton = styled(Button)(({ theme }) => ({
  backgroundColor: '#fff',
  '&:hover': {
    backgroundColor: theme.palette.primary.main,
    borderColor: theme.palette.primary.dark,
    color: '#fff',
  },
  border: 1,
  borderColor: theme.palette.primary.main,
  borderRadius: 8,
  // color: '#000',
  // width: '120px',
}))
