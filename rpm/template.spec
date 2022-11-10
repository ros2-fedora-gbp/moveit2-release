%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-moveit-setup-framework
Version:        2.6.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_setup_framework package

License:        BSD
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-rolling-ament-index-cpp
Requires:       ros-rolling-moveit-common
Requires:       ros-rolling-moveit-core
Requires:       ros-rolling-moveit-ros-planning
Requires:       ros-rolling-moveit-ros-visualization
Requires:       ros-rolling-pluginlib
Requires:       ros-rolling-rclcpp
Requires:       ros-rolling-rviz-common
Requires:       ros-rolling-rviz-rendering
Requires:       ros-rolling-srdfdom
Requires:       ros-rolling-urdf
Requires:       ros-rolling-ros-workspace
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-ament-index-cpp
BuildRequires:  ros-rolling-moveit-common
BuildRequires:  ros-rolling-moveit-core
BuildRequires:  ros-rolling-moveit-ros-planning
BuildRequires:  ros-rolling-moveit-ros-visualization
BuildRequires:  ros-rolling-pluginlib
BuildRequires:  ros-rolling-rclcpp
BuildRequires:  ros-rolling-rviz-common
BuildRequires:  ros-rolling-rviz-rendering
BuildRequires:  ros-rolling-srdfdom
BuildRequires:  ros-rolling-urdf
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-clang-format
BuildRequires:  ros-rolling-ament-cmake-lint-cmake
BuildRequires:  ros-rolling-ament-cmake-xmllint
BuildRequires:  ros-rolling-ament-lint-auto
%endif

%description
C++ Interface for defining setup steps for MoveIt Setup Assistant

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Thu Nov 10 2022 David V. Lu!! <davidvlu@gmail.com> - 2.6.0-1
- Autogenerated by Bloom

* Thu Jul 28 2022 David V. Lu!! <davidvlu@gmail.com> - 2.5.3-1
- Autogenerated by Bloom

* Mon Jul 25 2022 David V. Lu!! <davidvlu@gmail.com> - 2.5.2-1
- Autogenerated by Bloom

