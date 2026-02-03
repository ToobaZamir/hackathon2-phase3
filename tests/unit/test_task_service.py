import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session, select
from src.models.task import Task, TaskCreate, TaskUpdate
from src.services.task_service import TaskService
from src.core.error_handlers import TaskNotFoundError, DatabaseError

class TestTaskService:
    def test_create_task_success(self):
        """Test successful task creation"""
        # Mock data
        task_create = TaskCreate(
            title="Test Task",
            description="Test Description",
            completed=False,
            user_id=1
        )

        # Mock session
        mock_session = Mock(spec=Session)

        # Mock task instance
        mock_task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False,
            user_id=1
        )

        # Configure mock session
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()

        with patch.object(Task, 'model_validate', return_value=mock_task):
            result = TaskService.create_task(mock_session, task_create)

            # Verify session methods were called
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

            # Verify result
            assert result.id == 1
            assert result.title == "Test Task"

    def test_get_task_by_id_success(self):
        """Test successful task retrieval by ID"""
        # Mock session
        mock_session = Mock(spec=Session)

        # Mock task result
        mock_task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False,
            user_id=1
        )

        # Configure mock session execution
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = mock_task
        mock_session.exec.return_value = mock_exec_result

        result = TaskService.get_task_by_id(mock_session, 1, 1)

        # Verify session methods were called
        mock_session.exec.assert_called_once()
        assert result.id == 1
        assert result.title == "Test Task"

    def test_get_task_by_id_not_found(self):
        """Test task retrieval when task doesn't exist"""
        # Mock session
        mock_session = Mock(spec=Session)

        # Configure mock session execution to return None
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = None
        mock_session.exec.return_value = mock_exec_result

        # Should raise TaskNotFoundError
        with pytest.raises(TaskNotFoundError):
            TaskService.get_task_by_id(mock_session, 999, 1)

    def test_update_task_success(self):
        """Test successful task update"""
        # Mock data
        task_update = TaskUpdate(title="Updated Title")

        # Mock session
        mock_session = Mock(spec=Session)

        # Mock existing task
        mock_task = Task(
            id=1,
            title="Old Title",
            description="Test Description",
            completed=False,
            user_id=1
        )

        # Configure mock session execution
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = mock_task
        mock_session.exec.return_value = mock_exec_result

        # Mock the updated task
        updated_task = Task(
            id=1,
            title="Updated Title",
            description="Test Description",
            completed=False,
            user_id=1
        )

        with patch.object(Task, 'model_validate', return_value=updated_task):
            result = TaskService.update_task(mock_session, 1, 1, task_update)

            # Verify session methods were called
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

            # Verify the task was updated
            assert result.title == "Updated Title"

    def test_delete_task_success(self):
        """Test successful task deletion"""
        # Mock session
        mock_session = Mock(spec=Session)

        # Mock existing task
        mock_task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False,
            user_id=1
        )

        # Configure mock session execution
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = mock_task
        mock_session.exec.return_value = mock_exec_result

        # Configure mock session delete method
        mock_session.delete = Mock()
        mock_session.commit = Mock()

        result = TaskService.delete_task(mock_session, 1, 1)

        # Verify session methods were called
        mock_session.delete.assert_called_once()
        mock_session.commit.assert_called_once()
        assert result is True

    def test_toggle_task_completion_success(self):
        """Test successful task completion toggle"""
        # Mock session
        mock_session = Mock(spec=Session)

        # Mock existing task
        mock_task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=False,
            user_id=1
        )

        # Configure mock session execution
        mock_exec_result = Mock()
        mock_exec_result.first.return_value = mock_task
        mock_session.exec.return_value = mock_exec_result

        # Configure mock session methods
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()

        # Mock the updated task
        updated_task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            completed=True,
            user_id=1
        )

        with patch.object(Task, 'model_validate', return_value=updated_task):
            result = TaskService.toggle_task_completion(mock_session, 1, 1, True)

            # Verify session methods were called
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

            # Verify the task completion was updated
            assert result.completed is True