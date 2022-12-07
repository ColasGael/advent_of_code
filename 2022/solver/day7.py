from typing import List, Tuple


def main(
    input_lines: List[str],
    max_dir_size: int = 100000,
    total_disk_space: int = 70000000,
    min_free_space: int = 30000000,
) -> Tuple[int, int]:
    FileSystem.MAX_DIR_SIZE = max_dir_size
    root_fs = FileSystem.create(input_lines)

    part1_answer: int = sum(root_fs.part1_sizes)
    part2_answer: int = find_smallest_dir_to_delete(
        root_fs, total_disk_space, min_free_space
    )

    return part1_answer, part2_answer


class FileSystem(object):  # pylint: disable=useless-object-inheritance
    MAX_DIR_SIZE: int = -1

    _name: str
    _size: int
    # Remark: recursive class so use class name (str) for annotations
    _children: List["FileSystem"]

    part1_sizes: List[int]

    def __init__(self, name: str, size: int = 0) -> None:
        self._name = name
        self._size = size
        self._is_dir = self.size == 0
        self._children = []
        self.part1_sizes = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    @property
    def is_dir(self) -> bool:
        return self._is_dir

    @property
    def children(self) -> List["FileSystem"]:
        return self._children

    @property
    def children_names(self) -> List[str]:
        children_names = [child.name for child in self._children]
        return children_names

    def add_child(self, child: "FileSystem") -> None:
        assert (
            child.name not in self.children_names
        ), f"Cannot add child with name {child.name}, a child with the same name already exists"
        self._children.append(child)
        self._size += child.size

        # Remark: Could be done AFTER building the tree, by performing a depth-first search
        # But since that's what we are doing when building it, we can do everything at the same time
        self.part1_sizes += child.part1_sizes
        if child.is_dir and child.size <= self.MAX_DIR_SIZE:
            self.part1_sizes.append(child.size)

    @classmethod
    def create(cls, terminal_outputs: List[str]) -> "FileSystem":
        """Build a tree representation of the filesystem.
           From the result of commands exploring the said filesystem.

        Assumption:
            - Start at the root
            - Change 1 level of directory at a time
            - Explore all the directories
        """
        open_fs: List["FileSystem"] = []
        # Find the directory children
        for terminal_output in terminal_outputs:
            if terminal_output.startswith("$"):
                command = terminal_output[2:]
                if command.startswith("cd"):
                    dir_name = command[3:]
                    if dir_name == "..":
                        # Done exploring the current directory
                        child = open_fs.pop()
                        open_fs[-1].add_child(child)
                    else:
                        # Exploring a new directory
                        child = FileSystem(dir_name)
                        open_fs.append(child)
                # else:  command == "ls"
                # Result handled below
            else:  # Result of ls
                el_1, name = terminal_output.split(" ")
                if el_1 != "dir":  # file so 2nd element is the file size
                    child = FileSystem(name, int(el_1))
                    open_fs[-1].add_child(child)
                # else:  directory will be handled when exploring it

        # Done exploring the whole filesystem: finalize the open directories' relationships
        while len(open_fs) > 1:
            child = open_fs.pop()
            open_fs[-1].add_child(child)
        root_fs = open_fs[0]
        return root_fs


def find_smallest_dir_to_delete(
    root_fs: FileSystem, total_disk_space: int, min_free_space: int
) -> int:
    assert total_disk_space > min_free_space
    current_free_space = total_disk_space - root_fs.size
    # Depth-first search
    open_fs = [root_fs]
    deleted_dir_size = root_fs.size
    while len(open_fs) > 0:
        current_fs = open_fs.pop()
        for child in current_fs.children:
            if not child.is_dir:
                continue
            new_free_space = current_free_space + child.size
            if new_free_space < min_free_space:
                # Directory is too small
                # No need to process child directories as they would be smaller
                continue
            # Get the smallest directory that validates the constraint
            deleted_dir_size = min(child.size, deleted_dir_size)
            # Add the directory, in case some of it's children validates the constraint
            open_fs.append(child)
    return deleted_dir_size
