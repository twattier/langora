import { styled } from '@mui/system'

import Box from '@mui/material/Box'
import TextField from '@mui/material/TextField'

export const ContentBox = styled((props) => <Box {...props} />)(
  ({ theme }) => ({
    backgroundColor: theme.palette.content.main,
    border: '1px solid',
    borderColor: theme.palette.content.dark,
    borderRadius: '4px',
  })
)

export const InputQuery = styled((props) => <TextField {...props} />)(
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
